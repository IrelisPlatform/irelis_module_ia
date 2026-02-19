from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, desc, case
from app.models import Message, UserBlock, User
from app.schemas import MessageCreate
from uuid import UUID

class ChatRepository:
    def create_message(self, db: Session, message: MessageCreate) -> Message:
        db_message = Message(
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            content=message.content
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    def get_messages_between(self, db: Session, user1_id: UUID, user2_id: UUID):
        return db.query(Message).filter(
            or_(
                and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
                and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
            )
        ).order_by(Message.created_at.asc()).all()

    def get_conversations(self, db: Session, user_id: UUID):
        subquery = (
            db.query(
                Message.id,
                Message.sender_id,
                Message.receiver_id,
                Message.content,
                Message.created_at,
                func.row_number().over(
                    partition_by=(
                        func.least(Message.sender_id, Message.receiver_id),
                        func.greatest(Message.sender_id, Message.receiver_id)
                    ),
                    order_by=desc(Message.created_at)
                ).label("rn")
            )
            .filter(or_(Message.sender_id == user_id, Message.receiver_id == user_id))
            .cte("ranked_messages")
        )
        partner_id_col = case(
            (subquery.c.sender_id == user_id, subquery.c.receiver_id),
            else_=subquery.c.sender_id
        )

        return (
            db.query(subquery, User)
            .join(User, User.id == partner_id_col)
            .filter(subquery.c.rn == 1)
            .order_by(desc(subquery.c.created_at))
            .all()
        )
    def is_blocked(self, db: Session, user1_id: UUID, user2_id: UUID) -> bool:
        block = db.query(UserBlock).filter(
            or_(
                and_(UserBlock.blocker_id == user1_id, UserBlock.blocked_id == user2_id),
                and_(UserBlock.blocker_id == user2_id, UserBlock.blocked_id == user1_id)
            )
        ).first()
        return block is not None

    def toggle_block(self, db: Session, blocker_id: UUID, blocked_id: UUID):
        existing_block = db.query(UserBlock).filter(
            UserBlock.blocker_id == blocker_id,
            UserBlock.blocked_id == blocked_id
        ).first()

        if existing_block:
            db.delete(existing_block)
            db.commit()
            return False
        else:
            new_block = UserBlock(blocker_id=blocker_id, blocked_id=blocked_id)
            db.add(new_block)
            db.commit()
            return True