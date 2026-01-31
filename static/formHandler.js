function add_message(response){
	//funkcja dodaje wiadomość do tabelki, jeśli została ona pomyślnie zapisana w bazie danych
	var noMessagesParagraph = document.getElementById('no-messages');
	if(noMessagesParagraph != null){
		noMessagesParagraph.remove();
	}
	
	messageDiv = document.createElement('div');
	messageDiv.setAttribute('class', 'message');
	
	dateParagraph = document.createElement('p');
	dateParagraph.innerText = 'Date: ' + response['date'];

	authorParagraph = document.createElement('p');
	authorParagraph.innerText = 'Author: ' + response['username'];
	
	messageParagraph = document.createElement('p');
	messageParagraph.innerText = response['message'];
	
	messageDiv.appendChild(dateParagraph);
	messageDiv.appendChild(authorParagraph);
	messageDiv.appendChild(messageParagraph);
	
	messageList = document.getElementById('messages');
	messageList.prepend(messageDiv);
}

async function sendData(){
	//wysłanie danych z formularza na serwer
	const postForm = document.getElementById("addMessageForm");
	const dane = new FormData(postForm);
	var response = await fetch('/api/add', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(Object.fromEntries(dane))
	}
	);
	response = await response.json();
	if(response['response code'] === 200){
		add_message(response);
	}else{
		alert(response['status']);
	}
}