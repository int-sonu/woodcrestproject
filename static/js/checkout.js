function handlePlaceOrder() {
    // Check which payment method is selected
    const paymentMethod = document.querySelector('input[name="payment_method"]:checked');
    
    if (!paymentMethod) {
        // If no payment method is selected, show an alert
        alert("Please select a payment method before placing your order.");
        return;
    }

    if (paymentMethod.value === 'cash_on_delivery') {
        // Handle Cash on Delivery
        alert('Thank you for your order! Your order will be delivered soon.');
        window.location.href = "/thank-you/";  // Redirect to a thank-you page or show a success message
    } else if (paymentMethod.value === 'online_payment') {
        // Open Razorpay for online payment
        openRazorpay();
    }
}
function openRazorpay() {
var rawAmount = parseFloat("{{ grand_total|floatformat:2 }}");
var amountInPaise = Math.round(rawAmount * 100);

if (!Number.isInteger(amountInPaise) || amountInPaise <= 0) {
console.error("Amount in paise is not valid.");
return;
}

var options = {
"key": "rzp_test_kuS91ojzsMscI2",
"amount": amountInPaise,
"currency": "INR",
"name": "WoodCrest",
"description": "Payment for order",
"image": "{% static 'img/home/log10.png' %}",
"handler": function (response) {
    var paymentId = response.razorpay_payment_id;

    // Send the payment details to your server
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/your-server-endpoint/", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log("Payment details saved successfully:", xhr.responseText);
            window.location.href = "/thank-you/";  // Redirect after saving payment details
        } else {
            console.error("Error saving payment details:", xhr.statusText);
        }
    };
    xhr.send(JSON.stringify({ 
        payment_id: paymentId, 
        order_id: response.razorpay_order_id,
        amount: rawAmount  // Send the amount as well
    }));
},
"prefill": {
    "name": "{{ user.username }}",
    "email": "{{ user.email }}",
    "contact": "{{ user.mobile_number }}"
},
"theme": {
    "color": "#3399cc"
}
};
var rzp1 = new Razorpay(options);
rzp1.open();
}


// JavaScript for toggling the edit profile form
document.getElementById('edit-button').addEventListener('click', function() {
    var profileInfo = document.getElementById('profile-info');
    var editProfileForm = document.querySelector('.edit-profile-form');
    if (editProfileForm.style.display === 'none') {
        profileInfo.style.display = 'none';
        editProfileForm.style.display = 'block';
    } else {
        profileInfo.style.display = 'block';
        editProfileForm.style.display = 'none';
    }
});

document.getElementById('cancel-button').addEventListener('click', function() {
    var profileInfo = document.getElementById('profile-info');
    var editProfileForm = document.querySelector('.edit-profile-form');
    profileInfo.style.display = 'block';
    editProfileForm.style.display = 'none';
});