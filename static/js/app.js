document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.querySelector('input[name="transaction_date"]');
  if (dateInput && !dateInput.value) {
    const d = new Date();
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    dateInput.value = `${d.getFullYear()}-${month}-${day}`;
  }
});
