import graphene
from app.models import SessionLocal, Patient

class PatientType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    age = graphene.Int()
    diagnosis = graphene.String()

class Query(graphene.ObjectType):
    patients = graphene.List(PatientType)

    def resolve_patients(parent, info):
        db = SessionLocal()
        return db.query(Patient).all()

schema = graphene.Schema(query=Query)
