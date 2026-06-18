const form = document.getElementById("signupForm");
const formMessage = document.getElementById("formMessage");

const setMessage = (message, type) => {
  formMessage.textContent = message;
  formMessage.className = `form-message ${type ? `is-${type}` : ""}`.trim();
};

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const name = String(formData.get("name") || "").trim();
  const email = String(formData.get("email") || "").trim();
  const password = String(formData.get("password") || "");
  const confirmPassword = String(formData.get("confirmPassword") || "");
  const phone = String(formData.get("phone") || "").trim();
  const termsAccepted = formData.get("terms");

  if (!name || !email || !password || !confirmPassword || !phone) {
    setMessage("모든 필수 항목을 입력해 주세요.", "error");
    return;
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    setMessage("이메일 형식을 다시 확인해 주세요.", "error");
    return;
  }

  if (password.length < 8) {
    setMessage("비밀번호는 8자 이상이어야 합니다.", "error");
    return;
  }

  if (password !== confirmPassword) {
    setMessage("비밀번호가 일치하지 않습니다.", "error");
    return;
  }

  if (!/^01[0-9]-?\d{3,4}-?\d{4}$/.test(phone)) {
    setMessage("휴대폰 번호 형식을 확인해 주세요.", "error");
    return;
  }

  if (!termsAccepted) {
    setMessage("이용약관 동의가 필요합니다.", "error");
    return;
  }

  setMessage(`${name}님, 회원가입이 완료되었습니다.`, "success");
  form.reset();
});
