;
(() => {
  const $deleteForm = document.querySelector('.delete-form');

  document.querySelectorAll('.groups .close').forEach($a => {
    $a.addEventListener('click', e => {
      e.preventDefault();

      const $elem = e.currentTarget;
      const name = $elem.getAttribute('data-name');

      $deleteForm.action = `/groups/${name}?__method=DELETE`;
      $deleteForm.submit();
    }, false);
  });
})();
