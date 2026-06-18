const form = document.getElementById("signupForm");
const formMessage = document.getElementById("formMessage");

// 검증 결과를 한곳에서 갱신해 메시지 문구와 상태 클래스를 함께 관리한다.
const setMessage = (message, type) => {
  formMessage.textContent = message;
  formMessage.className = `form-message ${type ? `is-${type}` : ""}`.trim();
};

form.addEventListener("submit", (event) => {
  event.preventDefault();

  // 제출 시점의 입력값을 모아 공백 정리 후 검증에 사용한다.
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

  // 지나치게 엄격한 규칙 대신 일반적인 이메일 형식만 빠르게 확인한다.
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

  // 필수 약관 동의 여부는 마지막 단계에서 다시 확인한다.
  if (!termsAccepted) {
    setMessage("이용약관 동의가 필요합니다.", "error");
    return;
  }

  setMessage(`${name}님, 회원가입이 완료되었습니다.`, "success");
  form.reset();
});
