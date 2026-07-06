const form = document.getElementById('generateForm');
const button = document.getElementById('generateBtn');

if (form && button) {
  form.addEventListener('submit', () => {
    button.disabled = true;
    button.textContent = 'Processing files... Please wait';
  });
}
