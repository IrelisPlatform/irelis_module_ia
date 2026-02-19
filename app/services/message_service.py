from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.message_repository import ChatRepository
from app.schemas import MessageCreate, ConversationSummary
from uuid import UUID

class ChatService:
    def __init__(self,db):
        self.repo = ChatRepository()
        self.db = db

    def send_message(self, message: MessageCreate):
        if message.receiver_id == message.sender_id:
            raise HTTPException(status_code=400, detail="Impossible to send message to yourself.")

        if self.repo.is_blocked(self.db, message.sender_id, message.receiver_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You cannot send message to this user"
            )

        return self.repo.create_message(self.db, message)

    def get_history(self, current_user_id: UUID, other_user_id: UUID):
        return self.repo.get_messages_between(self.db, current_user_id, other_user_id)

    def get_inbox(self, current_user_id: UUID) -> list[ConversationSummary]:
        raw_conversations = self.repo.get_conversations(self.db, current_user_id)
        
        results = []
        for row in raw_conversations:
            # L'index 6 correspond à l'entité User retournée par la requête SQL
            message_data = row[0:6]
            partner_user = row[6] 
            
            # Identifier l'ID de l'interlocuteur
            other_id = message_data[2] if message_data[1] == current_user_id else message_data[1]
            partner_name = partner_user.email 
            
            # Si l'utilisateur est un candidat
            if partner_user.candidate:
                partner_name = f"{partner_user.candidate.first_name} {partner_user.candidate.last_name}"
            
            # Si l'utilisateur est un recruteur
            elif partner_user.recruiter:
                partner_name = f"{partner_user.recruiter.first_name} {partner_user.recruiter.last_name}"
            
            results.append(ConversationSummary(
                partner_id=other_id,
                partner_name=partner_name.strip(), # .strip() enlève les espaces en trop
                last_message=message_data[3],
                last_message_at=message_data[4],
                unread_count=0
            ))
            
        return results

    def toggle_block_user(self, current_user_id: UUID, target_user_id: UUID):
        if current_user_id == target_user_id:
            raise HTTPException(status_code=400, detail="Impossible to block yourself")
            
        return self.repo.toggle_block(self.db, current_user_id, target_user_id)