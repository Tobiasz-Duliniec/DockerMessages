function add_message(response){
	const noMessagesParagraph = document.getElementById('no-messages');
	if(noMessagesParagraph) noMessagesParagraph.remove();

	const messageDiv = document.createElement('article');
	messageDiv.className = 'message';
	messageDiv.setAttribute('aria-label', `Message by ${response.username}`);

	const meta = document.createElement('p');
	meta.className = 'meta';
	meta.innerHTML = `${response.date} — <strong>${escapeHtml(response.username)}</strong>`;

	const body = document.createElement('p');
	body.innerText = response.message;

	messageDiv.appendChild(meta);
	messageDiv.appendChild(body);

	const messageList = document.getElementById('messages');
	messageList.prepend(messageDiv);
}

function escapeHtml(str){
	return String(str).replace(/[&<>"']/g, function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[m]});
}

async function submitHandler(e){
	e.preventDefault();
	const form = document.getElementById('addMessageForm');
	const status = document.getElementById('form-status');
	const submitBtn = document.getElementById('submitBtn');

	const formData = new FormData(form);
	const payload = Object.fromEntries(formData.entries());

	submitBtn.disabled = true;
	status.textContent = 'Sending...';

	try{
		const res = await fetch('/api/add', {
			method: 'POST',
			headers: {'Content-Type':'application/json'},
			body: JSON.stringify(payload)
		});
		const json = await res.json();
		if(json['response code'] === 200){
			add_message(json);
			form.reset();
			status.textContent = 'Message added';
		} else {
			status.textContent = json['status'] || 'Error saving message';
		}
	}catch(err){
		status.textContent = 'Network error';
	}finally{
		submitBtn.disabled = false;
		setTimeout(()=>{status.textContent=''},3000);
	}
}

document.addEventListener('DOMContentLoaded', ()=>{
	const form = document.getElementById('addMessageForm');
	if(form) form.addEventListener('submit', submitHandler);
});