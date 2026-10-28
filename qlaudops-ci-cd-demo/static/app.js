(() => {
  const toast = document.getElementById('toast');
  let toastTimer;
  function notify(message) {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
  }
  document.getElementById('refresh-btn').addEventListener('click', async () => {
    const button = document.getElementById('refresh-btn');
    button.disabled = true;
    button.innerHTML = '<span>↻</span> Checking…';
    try {
      const response = await fetch('/health', {headers: {'Accept': 'application/json'}});
      if (!response.ok) throw new Error('Health check failed');
      const result = await response.json();
      notify(`System check complete: ${result.status}. Dashboard is up to date.`);
    } catch (error) {
      notify('Could not reach the application health endpoint. Check the server logs.');
    } finally {
      button.disabled = false;
      button.innerHTML = '<span>↻</span> Refresh data';
    }
  });
  document.getElementById('deploy-btn').addEventListener('click', () => {
    notify('Demo action: create a feature branch, push your change, then watch GitHub Actions run.');
    document.getElementById('deployments').scrollIntoView({behavior: 'smooth', block: 'center'});
  });
  document.querySelectorAll('.row-menu').forEach((button) => {
    button.addEventListener('click', () => notify(`${button.getAttribute('aria-label').replace('More actions for ', '')}: demo actions are read-only.`));
  });
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) {
        event.preventDefault();
        notify('This section is a visual demo placeholder.');
      }
    });
  });
  const dateLabel = document.getElementById('today-label');
  if (dateLabel) dateLabel.textContent = new Intl.DateTimeFormat('en-IN', {day: '2-digit', month: 'short', year: 'numeric'}).format(new Date()).toUpperCase();
})();
