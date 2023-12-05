;
(() => {
  const doc = document;
  doc.addEventListener('DOMContentLoaded', () => {
    doc.querySelector('.logout').addEventListener('click', e => {
      e.preventDefault();
      document.getElementById('logout-form').submit();
      return false;
    });
  });
})();
