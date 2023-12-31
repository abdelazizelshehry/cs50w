console.log("K")

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  console.log('api')

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = 'zz';
  document.querySelector('#compose-subject').value = 'zz';
  document.querySelector('#compose-body').value = 'zz';
  document.querySelector('#send-email').addEventListener('click', function(event) {
    event.preventDefault();
    console.log('Start API')
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
      fetch('/emails', {
        method: 'POST', 
        body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body,
          
        })
      }).then(response => response.json() )
        .then(result => {
        console.log(result);
        load_mailbox("sent");
      })
  },
  )
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}