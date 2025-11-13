"""
Smart tools - Sprint 1 version (Jira + GitHub only)
"""
from typing import Dict, Any, List
from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
import json
from src.tools.jira_tool import jira_tool
from src.tools.github_tool import github_tool
from src.config.settings import settings
from src.utils.logger import logger


class SmartToolOrchestrator:
    """Smart tools for Jira and GitHub only (Sprint 1)."""
    
    def __init__(self):
        self.llm = ChatMistralAI(
            model=settings.mistral_model,
            api_key=settings.mistral_api_key,
            temperature=0
        )
        logger.info("Smart Tool Orchestrator initialized (Sprint 1: Jira + GitHub)")
    
    def distill_ticket_decision(self, ticket_id: str) -> Dict[str, Any]:
        """Distill Jira ticket into key decision."""
        ticket = jira_tool.get_ticket_details(ticket_id)
        
        comments_text = "\n\n".join([
            f"Comment by {c.author} on {c.created}:\n{c.body}"
            for c in ticket.comments
        ])
        
        prompt = f"""You are analyzing a Jira ticket to extract the key technical decision.

Ticket: {ticket.key} - {ticket.summary}

Description:
{ticket.description}

Comments:
{comments_text}

Task: Extract the FINAL technical decision made in this ticket.

Return ONLY a JSON object with:
{{
    "decision": "One clear sentence describing what was decided",
    "rationale": "Why this decision was made",
    "decided_by": "Who made or approved the decision",
    "is_doc_worthy": true/false (is this important for user-facing documentation?),
    "category": "feature|bugfix|improvement|internal",
    "confidence": 0.0-1.0 (how clear is this decision?)
}}

If no clear decision was made, set confidence to 0.0.
"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            
            result["source_ticket"] = ticket_id
            result["ticket_status"] = ticket.status
            result["fix_versions"] = ticket.fix_versions
            
            logger.debug(f"Distilled {ticket_id}: {result['decision'][:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Failed to distill ticket {ticket_id}: {e}")
            return {
                "decision": f"Error processing ticket {ticket_id}",
                "confidence": 0.0,
                "is_doc_worthy": False
            }
    
    def distill_pr_impact(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """Distill GitHub PR into user impact."""
        pr = github_tool.get_pr_details(repo_name, pr_number)
        
        prompt = f"""You are analyzing a GitHub Pull Request to determine its impact.

PR #{pr.number}: {pr.title}

Description:
{pr.body or 'No description'}

Files Changed: {pr.files_changed}
Additions: {pr.additions}
Deletions: {pr.deletions}
Diff Summary: {pr.diff_summary}

Linked Issues: {', '.join(pr.linked_issues)}

Task: Determine the customer-facing impact of this PR.

Return ONLY a JSON object with:
{{
    "impact": "One sentence describing what changed for users",
    "impact_type": "feature|bugfix|performance|security|breaking_change|internal",
    "is_breaking": true/false,
    "is_doc_worthy": true/false,
    "technical_details": "Brief technical summary",
    "confidence": 0.0-1.0
}}

If this is purely internal/refactoring with no user impact, set is_doc_worthy to false.
"""
        
        try:
            response = self.llm.invoke(prompt)
            result = json.loads(response.content)
            
            result["source_pr"] = pr_number
            result["repo"] = repo_name
            result["merged_at"] = str(pr.merged_at) if pr.merged_at else None
            result["linked_issues"] = pr.linked_issues
            
            logger.debug(f"Distilled PR #{pr_number}: {result['impact'][:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Failed to distill PR {pr_number}: {e}")
            return {
                "impact": f"Error processing PR {pr_number}",
                "confidence": 0.0,
                "is_doc_worthy": False
            }
    
    def get_release_knowledge(self, release_version: str, project_name: str) -> Dict[str, Any]:
        """Smart aggregator for release (Jira + GitHub only)."""
        logger.info(f"Gathering smart knowledge for {release_version}")
        
        tickets = jira_tool.get_tickets_for_release(release_version)
        
        features = []
        bugfixes = []
        improvements = []
        breaking_changes = []
        
        for ticket in tickets:
            distilled = self.distill_ticket_decision(ticket.key)
            
            if not distilled.get("is_doc_worthy", False):
                continue
            
            prs = github_tool.find_prs_for_ticket(ticket.key)
            pr_impacts = []
            for pr in prs[:3]:
                impact = self.distill_pr_impact(pr.url.split('/')[-4] + '/' + pr.url.split('/')[-3], pr.number)
                if impact.get("is_doc_worthy"):
                    pr_impacts.append(impact)
            
            entry = {
                "ticket": ticket.key,
                "decision": distilled["decision"],
                "rationale": distilled["rationale"],
                "pr_impacts": pr_impacts,
                "confidence": distilled["confidence"]
            }
            
            category = distilled.get("category", "improvement")
            if category == "feature":
                features.append(entry)
            elif category == "bugfix":
                bugfixes.append(entry)
            elif category == "improvement":
                improvements.append(entry)
            
            if any(pr.get("is_breaking") for pr in pr_impacts):
                breaking_changes.append(entry)
        
        return {
            "release_version": release_version,
            "project": project_name,
            "features": features,
            "bugfixes": bugfixes,
            "improvements": improvements,
            "breaking_changes": breaking_changes,
            "total_tickets": len(tickets),
            "doc_worthy_items": len(features) + len(bugfixes) + len(improvements)
        }


# Global orchestrator
smart_orchestrator = SmartToolOrchestrator()


# LangChain tool wrappers
@tool
def get_smart_release_knowledge(release_version: str, project_name: str) -> str:
    """
    Get distilled release knowledge (Sprint 1: Jira + GitHub only).
    """
    knowledge = smart_orchestrator.get_release_knowledge(release_version, project_name)
    return json.dumps(knowledge, indent=2, default=str)


@tool
def get_ticket_decision_summary(ticket_id: str) -> str:
    """Get clean summary of Jira ticket decision."""
    summary = smart_orchestrator.distill_ticket_decision(ticket_id)
    return json.dumps(summary, indent=2)


@tool
def get_pr_impact_summary(repo_name: str, pr_number: int) -> str:
    """Get clean summary of PR impact."""
    summary = smart_orchestrator.distill_pr_impact(repo_name, pr_number)
    return json.dumps(summary, indent=2)

