(function () {
  const form = document.querySelector('form[data-teho-form]');
  if (!form) return;

  const endpoint = form.dataset.endpoint || window.TEHO_FORM_ENDPOINT;
  const successMessage = form.dataset.successMessage || 'Thanks! We\'ll be in touch within one business day.';
  const errorMessage = form.dataset.errorMessage || 'Something went wrong. Please email jack@teho.ai';
  const submitText = form.dataset.submitText || 'Submit request';

  const statusEl = document.createElement('p');
  statusEl.className = 'form-status';
  form.appendChild(statusEl);

  async function handleSubmit(event) {
    event.preventDefault();
    statusEl.textContent = '';
    const submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';
    }

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
      if (!endpoint) throw new Error('No endpoint configured');
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...payload,
          source: 'website',
          requested_at: new Date().toISOString(),
        }),
      });
      if (!res.ok) throw new Error('Non-200 response');
      statusEl.textContent = successMessage;
      statusEl.classList.add('form-status--success');
      form.reset();
    } catch (err) {
      console.error('Submission failed', err);
      statusEl.textContent = errorMessage;
      statusEl.classList.add('form-status--error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = submitText;
      }
    }
  }

  form.addEventListener('submit', handleSubmit);
})();
