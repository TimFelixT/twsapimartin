document.addEventListener('DOMContentLoaded',init_storage,false);
document.getElementById('stock_symb_submit').onclick = add_new_stock;
function add_new_stock(){
	var stock_symb= document.getElementById('stock_symb').value;
	var all_items = JSON.parse(localStorage.getItem('stock_symbols'));
	all_items.push(stock_symb);
	localStorage.setItem('stock_symbols', JSON.stringify(all_items));
	var list_body = document.getElementById('stock_list');
	var new_item = document.createEelement("li");
	new_item.className = 'list-group-item';
	new_item.textContent = i
	list_body.appendChild(new_item);


}

function display_symbol_list(){
	var list_body = document.getElementById('stock_list');
	var all_items = JSON.parse(localStorage.getItem('stock_symbols'))
	for (i in all_items)
	{
		var new_item = document.createElement('li');
		new_item.className = 'list-group-item';
		new_item.textContent = all_items[i]
		list_body.appendChild(new_item);
	}
}

function add_new_element(){
	var new_item = document.createEelement(li);
	new_item.className = 'list-group-item';
	new_item.textContent
}

function init_storage(){
	//localStorage.setItem('stock_symbols', JSON.stringify([]))
	if ( localStorage.getItem('stock_symbols') !== null) {
		console.log('Found Exisitng Storage');
	} else {
		console.log('Created new Storage');
		localStorage.setItem('stock_symbols', JSON.stringify([]))
	}
	display_symbol_list()
}