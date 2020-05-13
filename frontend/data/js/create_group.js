<<<<<<< HEAD
import { getCookie } from './load_user.js';
=======
// Get the modal
var modal = document.getElementById('createModal');

// Get the button that opens the modal
var btn = document.getElementById('createBtn');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName('close')[0];

// When the user clicks on the button, open the modal
btn.onclick = function () {
    modal.style.display = 'block';
    console.log(document.getElementById('group_name').value);
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = 'none';
};
>>>>>>> master

//API call
var btn2 = document.getElementById('create_form');

btn2.onclick = function () {
<<<<<<< HEAD
  let xhr = new XMLHttpRequest();
  xhr.open(
    'POST',
    'api/groups?session=' +
      getCookie('session_id') +
      '&group_name=' +
      document.getElementById('group_name').value
  );
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function () {
    if (xhr.status === 200) {
      var url_string = window.location;
      var url = new URL(url_string);
      var id = url.searchParams.get('group_id');
      window.location = 'group.html?group_id=' + id;
    }
  };
  xhr.send();
=======
    let xhr = new XMLHttpRequest();
    xhr.open(
        'POST',
        'api/groups?session=' +
        getCookie('session_id') +
        '&group_name=' +
        document.getElementById('group_name').value
    );
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log('group successfully created');
        }
    };
    xhr.send();
>>>>>>> master
};
