import { getCookie } from './load_user.js';
import { groupID } from './group_init.js';

//Get transaction modal
var modal = document.getElementById('transModal');
var btn = document.getElementById('transBtn');
var span = document.getElementById('close_trans_form');

// When the user clicks on the button, open the modal
btn.onclick = function () {
  modal.style.display = 'block';
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = 'none';
};

//API call
var btn2 = document.getElementById('submit_transaction');

btn2.onclick = function () {
  var url_string = window.location;
  var url = new URL(url_string);
  var id = url.searchParams.get('group_id');
  console.log(id);
  location.reload();

  //   let xhr = new XMLHttpRequest();
  //   xhr.open(
  //     'POST',
  //     'api/transactions?session=' +
  //       getCookie('session_id') +
  //       '&group_id=' + groupID + '&amount=' + document.getElementById('amount').value + '&paid=' +
  //   );
  //   xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  //   xhr.onload = function () {
  //     if (xhr.status === 200) {
  //       console.log('YOOOOOOO');
  //     }
  //   };
  //   xhr.send();
};
