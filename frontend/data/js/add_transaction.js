//display form
function relocate() {
  let url_string = window.location;
  let url = new URL(url_string);
  let group_id = url.searchParams.get('group_id');
  window.location = 'create_transaction.html?group_id=' + group_id;
}
