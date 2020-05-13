import { loadUser, configureGroups } from './load_user.js';

async function init_home() {
  let user = await loadUser();
  configureGroups();
}

$(document).ready(init_home());