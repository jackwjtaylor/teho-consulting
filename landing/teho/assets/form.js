(function () {
  const form = document.querySelector('form[data-teho-form]');
  if (!form) return;

  const endpoint = form.dataset.endpoint || window.TEHO_FORM_ENDPOINT;
  const supabaseUrl = form.dataset.supabaseUrl || window.TEHO_SUPABASE_URL;
  const supabaseKey = form.dataset.supabaseKey || window.TEHO_SUPABASE_KEY;
  const supabaseTable = form.dataset.supabaseTable || 'briefing_requests';
  const successMessage = form.dataset.successMessage || 'Thanks! We\'ll be in touch within one business day.';
  const errorMessage = form.dataset.errorMessage || 'Something went wrong. Please email jack@teho.ai';
  const submitText = form.dataset.submitText || 'Submit request';

  const statusEl = document.createElement('p');
  statusEl.className = 'form-status';
  form.appendChild(statusEl);

  async function safeRead(response) {
    try {
      const text = await response.clone().text();
      if (!text) return null;
      try {
        return JSON.parse(text);
      } catch (parseError) {
        return text;
      }
    } catch (error) {
      return null;
    }
  }

  function buildResponseError(status, payload) {
    let detail = '';
    if (payload && typeof payload === 'object') {
      detail = payload.message || JSON.stringify(payload);
    } else if (payload) {
      detail = payload;
    }
    return new Error(`HTTP ${status}${detail ? ` - ${detail}` : ''}`);
  }

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
    const slug = (payload.company || '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');

    try {
      let responseOk = false;
      let responsePayload = null;

      if (endpoint) {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...payload,
            source: 'website',
            requested_at: new Date().toISOString(),
          }),
        });
        responseOk = res.ok;
        responsePayload = await safeRead(res);
        if (!responseOk) {
          throw buildResponseError(res.status, responsePayload);
        }
        console.info('Public form submitted to custom endpoint', {
          endpoint,
          status: res.status,
        });
      } else if (supabaseUrl && supabaseKey) {
        const restUrl = `${supabaseUrl.replace(/\/$/, '')}/rest/v1/${supabaseTable}`;
        const res = await fetch(restUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            apikey: supabaseKey,
            Authorization: `Bearer ${supabaseKey}`,
            Prefer: 'return=minimal',
          },
          body: JSON.stringify({
            company_name: payload.company,
            slug: slug || `request-${Date.now()}`,
            domain: payload.domain || '',
            persona: payload.persona || '',
            primary_contact: payload.name || '',
            primary_email: payload.email || '',
            status: 'queued',
            priority: Number(payload.priority || 5) || 5,
            source: 'website',
            requested_at: new Date().toISOString(),
            payload: {
              name: payload.name || '',
              email: payload.email || '',
              objective: payload.objective || '',
              consent: Boolean(payload.consent),
            },
          }),
        });
        responseOk = res.ok;
        responsePayload = await safeRead(res);
        if (!responseOk) {
          throw buildResponseError(res.status, responsePayload);
        }
        console.info('Public form stored via Supabase REST', {
          status: res.status,
          restUrl,
        });
      } else {
        throw new Error('No endpoint configured');
      }

      statusEl.textContent = successMessage;
      statusEl.classList.add('form-status--success');
      form.reset();
    } catch (err) {
      console.error('Submission failed', err);
      if (err instanceof Error && err.message) {
        const message = err.message || '';
        if (message.includes('duplicate key') || message.includes('23505')) {
          statusEl.textContent =
            'It looks like that company is already queued. We\'ll refresh the data shortly.';
        } else {
          statusEl.textContent = `${errorMessage} (${message})`;
        }
      } else {
        statusEl.textContent = errorMessage;
      }
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
