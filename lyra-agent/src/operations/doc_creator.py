"""
Document creator - Sprint 1 version (release notes only).
"""
from pathlib import Path
from src.agents.controller import create_lyra_agent
from src.schemas.data_models import DocDraft
from src.config.settings import settings
from src.utils.logger import logger
from src.utils.metrics import AgentMetrics


class DocumentCreator:
    """Creates release notes using the agent."""
    
    def __init__(self):
        self.agent = create_lyra_agent()
        logger.info("Document Creator initialized (Sprint 1: release notes only)")
    
    def create_release_notes(self, release_version: str, project_name: str) -> DocDraft:
        """Create release notes for a specific version."""
        logger.info(f"Creating release notes for {project_name} {release_version}")
        
        metrics = AgentMetrics()
        
        initial_state = {
            "user_goal": f"Create comprehensive release notes for {project_name} version {release_version}",
            "doc_type": "release_notes",
            "release_version": release_version,
            "topic": None,
            "project_name": project_name,
            "messages": [],
            "knowledge_bundle": [],
            "sources_explored": [],
            "draft": None,
            "revision_count": 0,
            "critique_notes": "",
            "quality_score": 0.0,
            "approved": False,
            "next_action": "start",
            "iterations": 0,
            "max_iterations": settings.max_iterations
        }
        
        try:
            final_state = self.agent.invoke(initial_state)
            metrics.finish()
            metrics.iterations = final_state.get('iterations', 0)
            metrics.log_summary()
            
            draft = final_state.get('draft')
            if draft:
                self._save_draft(draft, project_name, "release_notes", release_version)
                return draft
            else:
                raise Exception("Agent failed to generate draft")
                
        except Exception as e:
            logger.error(f"Failed to create release notes: {e}")
            raise
    
    def _save_draft(self, draft: DocDraft, project_name: str, doc_type: str, identifier: str):
        """Save draft to output directory."""
        output_dir = Path(f"./outputs/generated_docs/{project_name}/{doc_type}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{identifier}.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(draft.content)
        
        logger.info(f"Draft saved to: {filepath}")


# Global instance
doc_creator = DocumentCreator()

