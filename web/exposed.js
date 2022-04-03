eel.expose(store_data);
function store_data(name,data) {
  localStorage.setItem(name,JSON.stringify(data))
}

eel.expose(send_data_py);
function send_data_py(name) {
  item = JSON.parse(localStorage.getsetItem(name,data))
  if (item !== null)
  { 
    return item
  } else
  { 
    return null;
  }
}

/*
eel.expose(trigger_crossing_py);
function trigger_crossing_py(symbols)
{
  //Color symbols in list which triggered a crossing red
}
*/