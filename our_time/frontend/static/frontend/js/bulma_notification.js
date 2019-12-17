// For FLASH MESSAGES - Makes it possible to click the (x) and close the notification
document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    $delete.addEventListener('click', (event) => {
      event.target.parentNode.remove();
    });
  });
});
