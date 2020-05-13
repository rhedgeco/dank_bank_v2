function init_inspect() {
  let url_string = window.location;
  let url = new URL(url_string);
  let id = url.searchParams.get('trans_id');
  console.log(id);

  let xhr = new XMLHttpRequest();
  xhr.open(
    'GET',
    'api/transactions?session=' + getCookie('session_id') + '&trans_id=' + id
  );
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function () {
    if (xhr.status === 200) {
      let trans_info = JSON.parse(xhr.responseText);
      document.getElementById('trans_content').innerText =
        '' +
        trans_info['payer'] +
        ' paid ' +
        trans_info['amount'] +
        ' for ' +
        trans_info['description'];

      let debtors = trans_info['paid'];
      let debt_list = document.getElementById('debtors');
      for (let i = 0; i < debtors.length; i++) {
        let debt_item = document.createElement('li');

        let debt_text = document.createElement('h5');
        debt_text.innerText = debtors[i];
        debt_item.appendChild(debt_text);

        debt_list.appendChild(debt_item);
      }
    }
  };
  xhr.send();
}

function goBack() {
  window.history.back();
}

$(document).ready(init_inspect());
