// Get create group modal
var modal1 = document.getElementById('createModal');
var btn1 = document.getElementById('createBtn');
var span1 = document.getElementById('close_group_form');

// When the user clicks on the button, open the modal
btn1.onclick = function () {
  modal1.style.display = 'block';
  console.log(document.getElementById('group_name').value);
};

// When the user clicks on <span> (x), close the modal
span1.onclick = function () {
  modal1.style.display = 'none';
};

//Get transaction modal
var modal2 = document.getElementById('transModal');
var btn2 = document.getElementById('transBtn');
var span2 = document.getElementById('close_trans_form');

// When the user clicks on the button, open the modal
btn2.onclick = function () {
  modal2.style.display = 'block';
};

// When the user clicks on <span> (x), close the modal
span2.onclick = function () {
  modal2.style.display = 'none';
};
