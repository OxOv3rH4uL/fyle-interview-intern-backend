from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]
    


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A
        },
        headers=h_principal
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == "FyleError"
    assert data["message"] == "assignment has not been submitted"


def test_grade_bad_assignment_principal(client,h_principal):
    """
    failure case: Assignment doesnt exist
    """
    response = client.get(
        '/principal/assignment/grade',
        json = {
            'id':1000000,
            'grade':'A'
        },
        headers = h_principal
    )
    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'NotFound'



def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_get_all_teacher(client,h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200
    data = response.json['data']
    for i in data:
        assert i['id'] is not None


def test_invalid_endpoint(client,h_principal):
    """
    failure case: Invalid endpoint in respective path
    """
    response = client.get(
        '/principal/abc',
        headers=h_principal
    )

    assert response.status_code == 404
    data = response.json
    assert data['error'] == "NotFound"


def test_student_endpoint(client,h_principal):
    """
    failure case: When principal is trying to get student endpoints
    """
    response = client.get(
        '/student/assignments',
        headers=h_principal
    )

    assert response.status_code == 403
    data = response.json
    assert data['error'] == "FyleError"
    assert data["message"] == "requester should be a student"

def test_teacher_endpoint(client,h_principal):
    """
    failure case: When principal is trying to get teacher endpoints
    """
    response = client.get(
        '/teacher/assignments',
        headers=h_principal
    )

    assert response.status_code == 403
    data = response.json
    assert data['error'] == "FyleError"
    assert data["message"] == "requester should be a teacher"
