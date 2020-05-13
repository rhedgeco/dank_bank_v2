import { loadUser, configureGroups } from './load_user.js';

window.onload = async function () {
  let user = await loadUser();
  configureGroups();
};
