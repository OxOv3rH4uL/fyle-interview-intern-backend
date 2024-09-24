import json

def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1



def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2




def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': ""
        })
    
    data = response.json
    assert response.status_code == 400
    assert data['error'] == 'FyleError'
    assert data['message'] == 'assignment with empty content cannot be submitted'



def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_post_assignment_student_2(client, h_student_2):
    content = 'ABCD TESTPOST Student 2'

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_update_assignment_null_content(client,h_student_1):
    content = ""

    response = client.post(
        '/student/assignments',
        headers = h_student_1,
        json = {
            'id':1,
            'content':""
        }
    )
    data = response.json
    assert response.status_code == 400
    assert data['error'] == 'FyleError'
    assert data['message'] == 'assignment with empty content cannot be submitted'

def test_submit_assignment_student_1_wrong_teacher(client,h_student_1):
    """
    failure case: When student tries to submit assignment to a teacher which is not found
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            "id":2,
            "teacher_id":4000
        }
    )

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Teacher not found!'


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200  
    data = response.json['data']
    assert data['student_id'] == 1
    assert data['id'] == 2
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2




def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'



def test_invalid_endpoint(client,h_student_1):
    """
    failure case: Invalid endpoint in respective path
    """
    response = client.get(
        '/student/abc',
        headers=h_student_1
    )

    assert response.status_code == 404
    data = response.json
    assert data['error'] == "NotFound"


def test_teacher_endpoint(client,h_student_1):
    """
    failure case: When student is trying to get teacher endpoints
    """
    response = client.get(
        '/teacher/assignments',
        headers=h_student_1
    )

    assert response.status_code == 403
    data = response.json
    assert data['error'] == "FyleError"
    assert data["message"] == "requester should be a teacher"

def test_principal_endpoint(client,h_student_1):
    """
    failure case: When student is trying to get principal endpoints
    """
    response = client.get(
        '/principal/assignments',
        headers=h_student_1
    )

    assert response.status_code == 403
    data = response.json
    assert data['error'] == "FyleError"
    assert data["message"] == "requester should be a principal"
