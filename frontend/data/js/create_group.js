// Get the modal
var modal = document.getElementById('createModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName('close')[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = 'none';
};

//API call
var btn2 = document.getElementById('create_form');

function create_group() {
    let element = document.getElementById('group_name').value;
    if(element === "") return;
    let xhr = new XMLHttpRequest();
    xhr.open(
        'POST',
        'api/groups?session=' +
        getCookie('session_id') +
        '&group_name=' +
        element
    );
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            window.location = 'group.html?group_id=' + xhr.responseText;
        }
    };
    xhr.send();
}

function create_btn_clicked() {
  modal.style.display = 'block';
  console.log(document.getElementById('group_name').value);
}
