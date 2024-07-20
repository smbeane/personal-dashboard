const clientId = "1d63c5cfdfd24410b1630dfb6a6d0e48";
const params = new URLSearchParams(window.location.search);
const code = "AQBpx1qcbOXBxzmrswJSvw4JtJNY8yBIt0NkZqBFjDXgjCaljSpx6rezhfZbekhdZDwZGBZsQpJea27S-bRbf3dukUve4DxQRFMat9JTDsgxTRM9YiPxZhpzFh9w7G77t4Q"
const clientSecret = "d316ab44da0d48f8aa238608bae2cd38"
if (!code) {
    redirectToAuthCodeFlow(clientId);
} else {
    const accessToken = await getAccessToken(clientId, code);
    const profile = await fetchProfile(accessToken);
    const player = await getPlayer(accessToken);
    console.log(profile);
    console.log(player)
    populateUI(profile, player);

}

export async function redirectToAuthCodeFlow(clientId) {
  const params = new URLSearchParams();
  params.append("client_id", clientId);
  params.append("response_type", "code");
  params.append("redirect_uri", "http://localhost:5173/callback");
  params.append("scope", "user-read-private user-read-email user-read-playback-state");

  document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
}

export async function getAccessToken(clientId, code) {
  const verifier = localStorage.getItem("verifier");

  const params = new URLSearchParams();
  params.append("client_id", clientId);
  params.append("grant_type", "authorization_code");
  params.append("code", code);
  params.append("redirect_uri", "http://localhost:5173/callback");
  params.append("code_verifier", verifier);

  const result = await fetch("https://accounts.spotify.com/api/token", {
      method: "POST",
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + (btoa(clientId + ':' + clientSecret))
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: code,
        client_id: clientId
      }),
  });
  const resultJson = await result.json();
  const { access_token } = resultJson;
  return access_token;
}

async function fetchProfile(token) {
  const result = await fetch("https://api.spotify.com/v1/me", {
      method: "GET", headers: { Authorization: `Bearer ${token}` }
  });

  return await result.json();
}

async function getPlayer(token){
  const result = await fetch("https://api.spotify.com/v1/me/player/currently-playing", {
    method: 'GET', headers: { Authorization: `Bearer ${token}` }
  });

  return await result.json();
}

function populateUI(profile, player) {
  document.getElementById("displayName").innerText = profile.display_name;
  if (profile.images[0]) {
      const profileImage = new Image(200, 200);
      profileImage.src = profile.images[0].url;
      document.getElementById("avatar").appendChild(profileImage);
      document.getElementById("imgUrl").innerText = profile.images[0].url;
  }
  document.getElementById("id").innerText = profile.id;
  document.getElementById("email").innerText = profile.email;
  document.getElementById("uri").innerText = profile.uri;
  document.getElementById("uri").setAttribute("href", profile.external_urls.spotify);
  document.getElementById("url").innerText = profile.href;
  document.getElementById("url").setAttribute("href", profile.href);
}