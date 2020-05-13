// function init_home() {
//     let xhr = new XMLHttpRequest();
//     xhr.open('GET', 'api/users?session=' + getCookie('session_id'));
//     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//     xhr.onload = function () {
//         if (xhr.status !== 200) {
//             window.location = '/';
//         }
//
//         if (xhr.status === 200) {
//             var json = JSON.parse(xhr.responseText);
//             console.log(json);
//             document.getElementById('main-text').innerText = json['nickname']; //retrieve and display nick name
//             document.getElementById('login-photo').src = json['photo'];
//         }
//     };
//     xhr.send();
// }
//
// window.onload = function () {
//     init_home();
// };
