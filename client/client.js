const stripe = Stripe("pk_test_WbTYwMTREEdIfb5y9r3ntwqg00lAIi9ipU");
const elements = stripe.elements();
const style = {
  base: {
    // Add your base input styles here. For example:
    fontSize: "16px",
    color: "#32325d"
  }
};

// Create an instance of the card Element.
const card = elements.create("card", { style });
card.mount("#card-element");

const form = document.getElementById("payment-form");
form.addEventListener("submit", async event => {
  event.preventDefault();

  const { paymentMethod, error } = await stripe.createPaymentMethod({
    type: "card",
    card: card,
    billing_details: {
      email: "hieuthai642@gmail.com"
    }
  });

  if (error) {
    console.log("[ERROR]");
    const errorElement = document.getElementById("card-errors");
    errorElement.textContent = error.message;
  } else {
    console.log("PAYMENT METHOD: ", paymentMethod);
    stripeTokenHandler(paymentMethod);
  }
});

card.addEventListener("change", ({ error }) => {
  const displayError = document.getElementById("card-errors");
  if (error) {
    displayError.textContent = error.message;
  } else {
    displayError.textContent = "";
  }
});

const stripeTokenHandler = async paymentMethod => {
  // Insert the token ID into the form so it gets submitted to the server
  const form = document.getElementById("payment-form");
  const hiddenInput = document.createElement("input");
  hiddenInput.setAttribute("type", "hidden");
  hiddenInput.setAttribute("name", "paymentMethod");
  hiddenInput.setAttribute("value", paymentMethod.id);
  form.appendChild(hiddenInput);
  form.submit();
};
