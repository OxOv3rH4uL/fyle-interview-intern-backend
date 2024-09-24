from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema,AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources',__name__)

@principal_assignments_resources.route('/assignments',methods=['GET'],strict_slashes=False)
@decorators.authenticate_principal
def get_all_assignments(p):
    all_assignments = Assignment.get_all_assignments()
    # print(all_assignments)
    all_assignments_dump = AssignmentSchema().dump(all_assignments,many=True)
    return APIResponse.respond(data=all_assignments_dump)


@principal_assignments_resources.route('/assignments/grade',methods=['POST'],strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p,incoming_payload):

    grade_payload = AssignmentGradeSchema().load(incoming_payload)

    grade_assignment = Assignment.mark_grade_principal(
        _id = grade_payload.id,
        grade = grade_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    changed_dump = AssignmentSchema().dump(grade_assignment)
    return APIResponse.respond(data=changed_dump)