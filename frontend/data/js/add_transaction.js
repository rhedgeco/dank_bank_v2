function relocate() {
  let url_string = window.location;
  let url = new URL(url_string);
  let group_id = url.searchParams.get('group_id');
  window.location = 'create_transaction.html?group_id=' + group_id;
}
let btn = document.getElementById('submit_transaction');

btn.addEventListener('click', () => {
  let url_string = window.location;
  let url = new URL(url_string);
  let group_id = url.searchParams.get('group_id');

  let amount = document.getElementById('paid').value;
  let desc = document.getElementById('desc').value;

  console.log(amount);
  console.log(desc);

  // let xhr = new XMLHttpRequest();
  // xhr.open(
  //   'POST',
  //   'api/transactions?session=' +
  //     getCookie('session_id') +
  //     '&group_id=' +
  //     group_id +
  //     '&amount=' +
  //     '&paid'
  // );
  // xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  // xhr.onload = function () {
  //   if (xhr.status === 200) {
  //     window.location = '/home.html';
  //   }
  // };
  // xhr.send();
});
