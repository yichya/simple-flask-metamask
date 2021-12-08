let provider;
let accounts;

let accountAddress = "";
let signer;

function multi_send() {
  fetch('multi_send').then(function (response) {
    return response.json();
  }).then(function (t) {
    console.log(t);
    delete t.gas;
    delete t.maxFeePerGas;
    delete t.maxPriorityFeePerGas;
    signer.sendTransaction(t).then(function (response) {
      console.log("signTransaction receipt", response.hash);
      fetch('receipt', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify([response.hash])
      }).then((response) => {
        return response.json();
      })
        .then((data) => {
          let m = ""
          for (let l of data) {
              m += `Sent: from ${l._from} to ${l.to} value ${l._value} wei\n`;
          }
          alert(m)
        });
    });
  });
}

function login() {
  console.log('oh hey there');
  rightnow = (Date.now() / 1000).toFixed(0)
  sortanow = rightnow - (rightnow % 600)
  signer.signMessage("Signing in to " + document.domain + " at " + sortanow, accountAddress, "test password!")
    .then((signature) => {
      handleAuth(accountAddress, signature)
    });
}

function handleAuth(accountAddress, signature) {
  console.log(accountAddress);
  console.log(signature);

  fetch('login', {
    method: 'post',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify([accountAddress, signature])
  }).then((response) => {
    return response.json();
  })
    .then((data) => {
      console.log(data);
      document.getElementById("login_first").textContent = "Logged in";
    });
}

ethereum.enable().then(function () {
  provider = new ethers.providers.Web3Provider(web3.currentProvider);
  provider.getNetwork().then(function (result) {
    console.log(result);
      provider.listAccounts().then(function (result) {
        console.log(result);
        accountAddress = result[0];
        provider.getBalance(String(result[0])).then(function (balance) {
          var myBalance = (balance / ethers.constants.WeiPerEther).toFixed(4);
          console.log("Your Balance: " + myBalance);
          document.getElementById("msg").textContent = 'Balance: ' + myBalance;
        });
        signer = provider.getSigner();
      })
  })
})
