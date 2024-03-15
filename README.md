# ⚠️ WARNING ⚠️

This doesn't actually work unless you're logged in. The result of the [Ajax request](https://github.com/loganmarchione/costco-pm-checker/blob/main/bot.py#L163-L165) is always this:

```
{ "errorCode": null, "errorMessage": "2-Day Delivery is currently not available in your area. Please visit your nearest <a href=\"/warehouse-locations\" class=\"body-copy-link\">Costco Warehouse</a> or visit our <a href=\"https://www.costco.com\" class=\"body-copy-link\">Grocery FAQs</a> for more information.", "errorMessageKey": "ERR_ZIP_NOTVALID", "errorMessageParam": null, "correctiveActionMessage": "", "correlationIdentifier": "-106cc8ca:18e3443e920:-1046", "exceptionData": { "Reason": "ZipCode is null or empty" }, "exceptionType": "0", "originatingCommand": "", "systemMessage": "" }
```

# costco-pm-checker

## Usage

1. Get code
    ```
    git clone https://github.com/loganmarchione/costco-pm-checker.git
    cd costco-pm-checker
    ```
1. Install Python requirements
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```
1. Make any changes you want to `URLs.txt`
1. Run the Python script 
    ```
    python3 bot.py
    ```

## Legal

This is a personal project that is not monetized. It is not endorsed by or affiliated with Costco in any way, and it is most definitely against Costco's terms of service.
