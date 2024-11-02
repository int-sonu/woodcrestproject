// static/js/sprofile.js
function showSection2() {
    document.getElementById('section-1').classList.add('hidden');
    document.getElementById('section-2').classList.remove('hidden');
}

function showSection1() {
    document.getElementById('section-2').classList.add('hidden');
    document.getElementById('section-1').classList.remove('hidden');
}

function showSection3() {
    document.getElementById('section-2').classList.add('hidden');
    document.getElementById('section-3').classList.remove('hidden');
}

function showSection4() {
    document.getElementById('section-3').classList.add('hidden');
    document.getElementById('section-4').classList.remove('hidden');
}

// static/js/sprofile.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profileForm');

    function showSection(sectionId) {
        document.querySelectorAll('.form-section').forEach(section => {
            section.classList.add('hidden');
        });
        document.getElementById(sectionId).classList.remove('hidden');
    }

    function validateName() {
        const name = document.getElementById('name').value.trim();
        const errorElement = document.getElementById('nameError');
        if (name === '' || /\s/.test(name) || !/^[a-zA-Z\s]+$/.test(name)) {
            errorElement.textContent = 'Name is required and should only contain alphabets and spaces.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validatePhone() {
        const phone = document.getElementById('phone').value.trim();
        const errorElement = document.getElementById('phoneError');
        if (phone === '' || !/^[6-9]\d{9}$/.test(phone)) {
            errorElement.textContent = 'Mobile number is required, must start with 6, 7, 8, or 9, and contain exactly 10 digits.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateEmail() {
        const email = document.getElementById('email').value.trim();
        const errorElement = document.getElementById('emailError');
        if (email === '' || !/^\S+@gmail\.com$/.test(email)) {
            errorElement.textContent = 'Email is required and must be a valid Gmail address.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateAddress() {
        const address = document.getElementById('address').value.trim();
        const errorElement = document.getElementById('addressError');
        if (address === '' || /\s/.test(address)) {
            errorElement.textContent = 'Address is required and should not contain whitespace.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateCity() {
        const city = document.getElementById('city').value.trim();
        const errorElement = document.getElementById('cityError');
        if (city === '' || /\s/.test(city) || !/^[a-zA-Z\s]+$/.test(city)) {
            errorElement.textContent = 'City is required and should only contain alphabets and spaces.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validatePincode() {
        const pincode = document.getElementById('pincode').value.trim();
        const errorElement = document.getElementById('pincodeError');
        if (pincode === '' || !/^\d{6}$/.test(pincode)) {
            errorElement.textContent = 'Pincode is required and must be exactly 6 digits.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validatePassword() {
        const password = document.getElementById('password').value.trim();
        const errorElement = document.getElementById('passwordError');
        if (password === '' || password.length < 6) {
            errorElement.textContent = 'Password is required and must be at least 6 characters long.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateBusinessName() {
        const businessName = document.getElementById('business-name').value.trim();
        const errorElement = document.getElementById('businessNameError');
        if (businessName === '' || /\s/.test(businessName) || !/^[A-Z][a-zA-Z\s]*$/.test(businessName)) {
            errorElement.textContent = 'Business Name is required and should start with a capital letter.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateGSTNumber() {
        const gstNumber = document.getElementById('gst-number').value.trim();
        const errorElement = document.getElementById('gstNumberError');
        if (gstNumber === '' || !/^[0-9]{15}$/.test(gstNumber)) {
            errorElement.textContent = 'GST Number is required and must be exactly 15 digits.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateBusinessPanCard() {
        const businessPanCard = document.getElementById('business-pan-card').value.trim();
        const errorElement = document.getElementById('businessPanCardError');
        if (businessPanCard === '' || !/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(businessPanCard)) {
            errorElement.textContent = 'Business PAN Card is required and must be a valid PAN number format.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateChequePassbookPhoto() {
        const chequePassbookPhoto = document.getElementById('cheque-passbook-photo').files.length;
        const errorElement = document.getElementById('chequePassbookPhotoError');
        if (chequePassbookPhoto === 0) {
            errorElement.textContent = 'Please upload a Cancel Cheque/Passbook Photo.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateAccountHolderName() {
        const accountHolderName = document.getElementById('account-holder-name').value.trim();
        const errorElement = document.getElementById('accountHolderNameError');
        if (accountHolderName === '' || /\s/.test(accountHolderName) || !/^[a-zA-Z\s]+$/.test(accountHolderName)) {
            errorElement.textContent = 'Account Holder Name is required and should only contain alphabets and spaces.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    function validateAccountNumber() {
        const accountNumber = document.getElementById('account-number').value.trim();
        const errorElement = document.getElementById('accountNumberError');
        if (accountNumber === '' || !/^\d{10}$/.test(accountNumber)) {
            errorElement.textContent = 'Account Number is required and must be exactly 10 digits.';
            return false;
        }
        errorElement.textContent = '';
        return true;
    }

    document.getElementById('name').addEventListener('input', validateName);
    document.getElementById('phone').addEventListener('input', validatePhone);
    document.getElementById('email').addEventListener('input', validateEmail);
    document.getElementById('address').addEventListener('input', validateAddress);
    document.getElementById('city').addEventListener('input', validateCity);
    document.getElementById('pincode').addEventListener('input', validatePincode);
    document.getElementById('password').addEventListener('input', validatePassword);
    document.getElementById('business-name').addEventListener('input', validateBusinessName);
    document.getElementById('gst-number').addEventListener('input', validateGSTNumber);
    document.getElementById('business-pan-card').addEventListener('input', validateBusinessPanCard);
    document.getElementById('cheque-passbook-photo').addEventListener('change', validateChequePassbookPhoto);
    document.getElementById('account-holder-name').addEventListener('input', validateAccountHolderName);
    document.getElementById('account-number').addEventListener('input', validateAccountNumber);

    form.addEventListener('submit', function(event) {
        let valid = validateName() &&
                    validatePhone() &&
                    validateEmail() &&
                    validateAddress() &&
                    validateCity() &&
                    validatePincode() &&
                    validatePassword() &&
                    validateBusinessName() &&
                    validateGSTNumber() &&
                    validateBusinessPanCard() &&
                    validateChequePassbookPhoto() &&
                    validateAccountHolderName() &&
                    validateAccountNumber();

        if (!valid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
});
