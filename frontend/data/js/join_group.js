function join_group() {
    let group_id = document.getElementById('group_code').value;
    let xhr = new XMLHttpRequest();
    xhr.open('PUT', 'api/groups?session='+getCookie('session_id')+'&group_id='+group_id);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            window.location = '/home.html'
        }
    };
    xhr.send();
}