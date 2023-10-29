;
(() => {
  const $deleteForm = document.getElementById('delete-form');

  function doDelete(e) {
    e.preventDefault();

    const $elem = e.currentTarget;
    $elem.removeEventListener('click', this);

    $deleteForm.action = `${$elem.getAttribute('data-id')}?__method=DELETE`;
    $deleteForm.submit();
    return false;
  }

  document.querySelectorAll('a.delete').forEach($a => {
    $a.addEventListener('click', doDelete, false);
  });
})();
