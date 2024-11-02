document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');

    signupForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting immediately

        if (!isValidUsername(signupForm.username.value)) {
            showError('Please enter a valid username.');
            return;
        }

        if (!isValidEmail(signupForm.email.value)) {
            showError('Please enter a valid email address.');
            return;
        }

        if (!isValidMobileNumber(signupForm.mobile_number.value)) {
            showError('Please enter a valid mobile number (starting with 9, 8, 7, or 6 and containing 10 digits).');
            return;
        }

        if (!isValidPincode(signupForm.pincode.value)) {
            showError('Please enter a valid 6-digit pincode.');
            return;
        }

        if (!isValidAddress(signupForm.address.value)) {
            showError('Please enter a valid address.');
            return;
        }

        if (!isValidPassword(signupForm.password.value)) {
            showError('Password must be at least 8 characters long.');
            return;
        }

        checkUsernameAvailability(signupForm.username.value)
            .then(isAvailable => {
                if (!isAvailable) {
                    showError('Username is already taken.');
                    return;
                }

                // If all checks pass, submit the form
                signupForm.submit();
            })
            .catch(error => {
                console.error('Error checking username availability:', error);
            });
    });

    function isValidUsername(username) {
        return username.trim().length > 0;
    }

    function isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const domainRegex = /^[^\s@]+@[^\s@]+\.[com]{3}$/;
        return regex.test(email) && domainRegex.test(email);
    }

    function isValidMobileNumber(mobileNumber) {
        return /^[7896]\d{9}$/.test(mobileNumber);
    }

    function isValidPincode(pincode) {
        return /^\d{6}$/.test(pincode);
    }

    function isValidAddress(address) {
        return address.trim().length > 0;
    }

    function isValidPassword(password) {
        return password.length >= 8;
    }

    function showError(message) {
        alert(message); // Display the error message in an alert box
    }

    function checkUsernameAvailability(username) {
        return fetch(`/check_username?username=${encodeURIComponent(username)}`)
            .then(response => response.json())
            .then(data => data.isAvailable);
    }
});
