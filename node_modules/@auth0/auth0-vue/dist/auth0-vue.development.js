(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('vue')) :
  typeof define === 'function' && define.amd ? define(['vue'], factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.vueAuth0 = factory(global.Vue));
})(this, (function (vue) { 'use strict';

  /**
   * @ignore
   */
  const AUTH0_TOKEN = '$auth0';
  /**
   * Injection token used to `provide` the `Auth0VueClient` instance. Can be used to pass to `inject()`
   *
   * ```js
   * inject(AUTH0_INJECTION_KEY)
   * ```
   */
  const AUTH0_INJECTION_KEY = Symbol(AUTH0_TOKEN);

  var version = '2.3.1';

  function e(e,t){var i={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(i[o]=e[o]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var n=0;for(o=Object.getOwnPropertySymbols(e);n<o.length;n++)t.indexOf(o[n])<0&&Object.prototype.propertyIsEnumerable.call(e,o[n])&&(i[o[n]]=e[o[n]]);}return i}"function"==typeof SuppressedError&&SuppressedError;var t="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{};function i(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}function o(e,t){return e(t={exports:{}},t.exports),t.exports}var n=o((function(e,t){Object.defineProperty(t,"__esModule",{value:!0});var i=function(){function e(){var e=this;this.locked=new Map,this.addToLocked=function(t,i){var o=e.locked.get(t);void 0===o?void 0===i?e.locked.set(t,[]):e.locked.set(t,[i]):void 0!==i&&(o.unshift(i),e.locked.set(t,o));},this.isLocked=function(t){return e.locked.has(t)},this.lock=function(t){return new Promise((function(i,o){e.isLocked(t)?e.addToLocked(t,i):(e.addToLocked(t),i());}))},this.unlock=function(t){var i=e.locked.get(t);if(void 0!==i&&0!==i.length){var o=i.pop();e.locked.set(t,i),void 0!==o&&setTimeout(o,0);}else e.locked.delete(t);};}return e.getInstance=function(){return void 0===e.instance&&(e.instance=new e),e.instance},e}();t.default=function(){return i.getInstance()};}));i(n);var a=i(o((function(e,i){var o=t&&t.__awaiter||function(e,t,i,o){return new(i||(i=Promise))((function(n,a){function r(e){try{c(o.next(e));}catch(e){a(e);}}function s(e){try{c(o.throw(e));}catch(e){a(e);}}function c(e){e.done?n(e.value):new i((function(t){t(e.value);})).then(r,s);}c((o=o.apply(e,t||[])).next());}))},a=t&&t.__generator||function(e,t){var i,o,n,a,r={label:0,sent:function(){if(1&n[0])throw n[1];return n[1]},trys:[],ops:[]};return a={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(a[Symbol.iterator]=function(){return this}),a;function s(a){return function(s){return function(a){if(i)throw new TypeError("Generator is already executing.");for(;r;)try{if(i=1,o&&(n=2&a[0]?o.return:a[0]?o.throw||((n=o.return)&&n.call(o),0):o.next)&&!(n=n.call(o,a[1])).done)return n;switch(o=0,n&&(a=[2&a[0],n.value]),a[0]){case 0:case 1:n=a;break;case 4:return r.label++,{value:a[1],done:!1};case 5:r.label++,o=a[1],a=[0];continue;case 7:a=r.ops.pop(),r.trys.pop();continue;default:if(!(n=r.trys,(n=n.length>0&&n[n.length-1])||6!==a[0]&&2!==a[0])){r=0;continue}if(3===a[0]&&(!n||a[1]>n[0]&&a[1]<n[3])){r.label=a[1];break}if(6===a[0]&&r.label<n[1]){r.label=n[1],n=a;break}if(n&&r.label<n[2]){r.label=n[2],r.ops.push(a);break}n[2]&&r.ops.pop(),r.trys.pop();continue}a=t.call(e,r);}catch(e){a=[6,e],o=0;}finally{i=n=0;}if(5&a[0])throw a[1];return {value:a[0]?a[1]:void 0,done:!0}}([a,s])}}},r=t;Object.defineProperty(i,"__esModule",{value:!0});var s="browser-tabs-lock-key",c={key:function(e){return o(r,void 0,void 0,(function(){return a(this,(function(e){throw new Error("Unsupported")}))}))},getItem:function(e){return o(r,void 0,void 0,(function(){return a(this,(function(e){throw new Error("Unsupported")}))}))},clear:function(){return o(r,void 0,void 0,(function(){return a(this,(function(e){return [2,window.localStorage.clear()]}))}))},removeItem:function(e){return o(r,void 0,void 0,(function(){return a(this,(function(e){throw new Error("Unsupported")}))}))},setItem:function(e,t){return o(r,void 0,void 0,(function(){return a(this,(function(e){throw new Error("Unsupported")}))}))},keySync:function(e){return window.localStorage.key(e)},getItemSync:function(e){return window.localStorage.getItem(e)},clearSync:function(){return window.localStorage.clear()},removeItemSync:function(e){return window.localStorage.removeItem(e)},setItemSync:function(e,t){return window.localStorage.setItem(e,t)}};function d(e){return new Promise((function(t){return setTimeout(t,e)}))}function u(e){for(var t="0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz",i="",o=0;o<e;o++){i+=t[Math.floor(Math.random()*t.length)];}return i}var l=function(){function e(t){this.acquiredIatSet=new Set,this.storageHandler=void 0,this.id=Date.now().toString()+u(15),this.acquireLock=this.acquireLock.bind(this),this.releaseLock=this.releaseLock.bind(this),this.releaseLock__private__=this.releaseLock__private__.bind(this),this.waitForSomethingToChange=this.waitForSomethingToChange.bind(this),this.refreshLockWhileAcquired=this.refreshLockWhileAcquired.bind(this),this.storageHandler=t,void 0===e.waiters&&(e.waiters=[]);}return e.prototype.acquireLock=function(t,i){return void 0===i&&(i=5e3),o(this,void 0,void 0,(function(){var o,n,r,l,h,p,m;return a(this,(function(a){switch(a.label){case 0:o=Date.now()+u(4),n=Date.now()+i,r=s+"-"+t,l=void 0===this.storageHandler?c:this.storageHandler,a.label=1;case 1:return Date.now()<n?[4,d(30)]:[3,8];case 2:return a.sent(),null!==l.getItemSync(r)?[3,5]:(h=this.id+"-"+t+"-"+o,[4,d(Math.floor(25*Math.random()))]);case 3:return a.sent(),l.setItemSync(r,JSON.stringify({id:this.id,iat:o,timeoutKey:h,timeAcquired:Date.now(),timeRefreshed:Date.now()})),[4,d(30)];case 4:return a.sent(),null!==(p=l.getItemSync(r))&&(m=JSON.parse(p)).id===this.id&&m.iat===o?(this.acquiredIatSet.add(o),this.refreshLockWhileAcquired(r,o),[2,!0]):[3,7];case 5:return e.lockCorrector(void 0===this.storageHandler?c:this.storageHandler),[4,this.waitForSomethingToChange(n)];case 6:a.sent(),a.label=7;case 7:return o=Date.now()+u(4),[3,1];case 8:return [2,!1]}}))}))},e.prototype.refreshLockWhileAcquired=function(e,t){return o(this,void 0,void 0,(function(){var i=this;return a(this,(function(r){return setTimeout((function(){return o(i,void 0,void 0,(function(){var i,o,r;return a(this,(function(a){switch(a.label){case 0:return [4,n.default().lock(t)];case 1:return a.sent(),this.acquiredIatSet.has(t)?(i=void 0===this.storageHandler?c:this.storageHandler,null===(o=i.getItemSync(e))?(n.default().unlock(t),[2]):((r=JSON.parse(o)).timeRefreshed=Date.now(),i.setItemSync(e,JSON.stringify(r)),n.default().unlock(t),this.refreshLockWhileAcquired(e,t),[2])):(n.default().unlock(t),[2])}}))}))}),1e3),[2]}))}))},e.prototype.waitForSomethingToChange=function(t){return o(this,void 0,void 0,(function(){return a(this,(function(i){switch(i.label){case 0:return [4,new Promise((function(i){var o=!1,n=Date.now(),a=!1;function r(){if(a||(window.removeEventListener("storage",r),e.removeFromWaiting(r),clearTimeout(s),a=!0),!o){o=!0;var t=50-(Date.now()-n);t>0?setTimeout(i,t):i(null);}}window.addEventListener("storage",r),e.addToWaiting(r);var s=setTimeout(r,Math.max(0,t-Date.now()));}))];case 1:return i.sent(),[2]}}))}))},e.addToWaiting=function(t){this.removeFromWaiting(t),void 0!==e.waiters&&e.waiters.push(t);},e.removeFromWaiting=function(t){void 0!==e.waiters&&(e.waiters=e.waiters.filter((function(e){return e!==t})));},e.notifyWaiters=function(){void 0!==e.waiters&&e.waiters.slice().forEach((function(e){return e()}));},e.prototype.releaseLock=function(e){return o(this,void 0,void 0,(function(){return a(this,(function(t){switch(t.label){case 0:return [4,this.releaseLock__private__(e)];case 1:return [2,t.sent()]}}))}))},e.prototype.releaseLock__private__=function(t){return o(this,void 0,void 0,(function(){var i,o,r,d;return a(this,(function(a){switch(a.label){case 0:return i=void 0===this.storageHandler?c:this.storageHandler,o=s+"-"+t,null===(r=i.getItemSync(o))?[2]:(d=JSON.parse(r)).id!==this.id?[3,2]:[4,n.default().lock(d.iat)];case 1:a.sent(),this.acquiredIatSet.delete(d.iat),i.removeItemSync(o),n.default().unlock(d.iat),e.notifyWaiters(),a.label=2;case 2:return [2]}}))}))},e.lockCorrector=function(t){for(var i=Date.now()-5e3,o=t,n=[],a=0;;){var r=o.keySync(a);if(null===r)break;n.push(r),a++;}for(var c=!1,d=0;d<n.length;d++){var u=n[d];if(u.includes(s)){var l=o.getItemSync(u);if(null!==l){var h=JSON.parse(l);(void 0===h.timeRefreshed&&h.timeAcquired<i||void 0!==h.timeRefreshed&&h.timeRefreshed<i)&&(o.removeItemSync(u),c=!0);}}}c&&e.notifyWaiters();},e.waiters=void 0,e}();i.default=l;})));const r={timeoutInSeconds:60},s={name:"auth0-spa-js",version:"2.1.3"},c=()=>Date.now();class d extends Error{constructor(e,t){super(t),this.error=e,this.error_description=t,Object.setPrototypeOf(this,d.prototype);}static fromPayload({error:e,error_description:t}){return new d(e,t)}}class u extends d{constructor(e,t,i,o=null){super(e,t),this.state=i,this.appState=o,Object.setPrototypeOf(this,u.prototype);}}class l extends d{constructor(){super("timeout","Timeout"),Object.setPrototypeOf(this,l.prototype);}}class h extends l{constructor(e){super(),this.popup=e,Object.setPrototypeOf(this,h.prototype);}}class p extends d{constructor(e){super("cancelled","Popup closed"),this.popup=e,Object.setPrototypeOf(this,p.prototype);}}class m extends d{constructor(e,t,i){super(e,t),this.mfa_token=i,Object.setPrototypeOf(this,m.prototype);}}class f extends d{constructor(e,t){super("missing_refresh_token",`Missing Refresh Token (audience: '${g(e,["default"])}', scope: '${g(t)}')`),this.audience=e,this.scope=t,Object.setPrototypeOf(this,f.prototype);}}function g(e,t=[]){return e&&!t.includes(e)?e:""}const w=()=>window.crypto,y=()=>{const e="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_~.";let t="";return Array.from(w().getRandomValues(new Uint8Array(43))).forEach((i=>t+=e[i%e.length])),t},k=e=>btoa(e),v=t=>{var{clientId:i}=t,o=e(t,["clientId"]);return new URLSearchParams((e=>Object.keys(e).filter((t=>void 0!==e[t])).reduce(((t,i)=>Object.assign(Object.assign({},t),{[i]:e[i]})),{}))(Object.assign({client_id:i},o))).toString()},b=e=>(e=>decodeURIComponent(atob(e).split("").map((e=>"%"+("00"+e.charCodeAt(0).toString(16)).slice(-2))).join("")))(e.replace(/_/g,"/").replace(/-/g,"+")),_=async(e,t)=>{const i=await fetch(e,t);return {ok:i.ok,json:await i.json()}},I=async(e,t,i)=>{const o=new AbortController;let n;return t.signal=o.signal,Promise.race([_(e,t),new Promise(((e,t)=>{n=setTimeout((()=>{o.abort(),t(new Error("Timeout when executing 'fetch'"));}),i);}))]).finally((()=>{clearTimeout(n);}))},S=async(e,t,i,o,n,a,r)=>{return s={auth:{audience:t,scope:i},timeout:n,fetchUrl:e,fetchOptions:o,useFormData:r},c=a,new Promise((function(e,t){const i=new MessageChannel;i.port1.onmessage=function(o){o.data.error?t(new Error(o.data.error)):e(o.data),i.port1.close();},c.postMessage(s,[i.port2]);}));var s,c;},O=async(e,t,i,o,n,a,r=1e4)=>n?S(e,t,i,o,r,n,a):I(e,o,r);async function T(t,i){var{baseUrl:o,timeout:n,audience:a,scope:r,auth0Client:c,useFormData:u}=t,l=e(t,["baseUrl","timeout","audience","scope","auth0Client","useFormData"]);const h=u?v(l):JSON.stringify(l);return await async function(t,i,o,n,a,r,s){let c,u=null;for(let e=0;e<3;e++)try{c=await O(t,o,n,a,r,s,i),u=null;break}catch(e){u=e;}if(u)throw u;const l=c.json,{error:h,error_description:p}=l,g=e(l,["error","error_description"]),{ok:w}=c;if(!w){const e=p||`HTTP error. Unable to fetch ${t}`;if("mfa_required"===h)throw new m(h,e,g.mfa_token);if("missing_refresh_token"===h)throw new f(o,n);throw new d(h||"request_error",e)}return g}(`${o}/oauth/token`,n,a||"default",r,{method:"POST",body:h,headers:{"Content-Type":u?"application/x-www-form-urlencoded":"application/json","Auth0-Client":btoa(JSON.stringify(c||s))}},i,u)}const j=(...e)=>{return (t=e.filter(Boolean).join(" ").trim().split(/\s+/),Array.from(new Set(t))).join(" ");var t;};class C{constructor(e,t="@@auth0spajs@@",i){this.prefix=t,this.suffix=i,this.clientId=e.clientId,this.scope=e.scope,this.audience=e.audience;}toKey(){return [this.prefix,this.clientId,this.audience,this.scope,this.suffix].filter(Boolean).join("::")}static fromKey(e){const[t,i,o,n]=e.split("::");return new C({clientId:i,scope:n,audience:o},t)}static fromCacheEntry(e){const{scope:t,audience:i,client_id:o}=e;return new C({scope:t,audience:i,clientId:o})}}class z{set(e,t){localStorage.setItem(e,JSON.stringify(t));}get(e){const t=window.localStorage.getItem(e);if(t)try{return JSON.parse(t)}catch(e){return}}remove(e){localStorage.removeItem(e);}allKeys(){return Object.keys(window.localStorage).filter((e=>e.startsWith("@@auth0spajs@@")))}}class P{constructor(){this.enclosedCache=function(){let e={};return {set(t,i){e[t]=i;},get(t){const i=e[t];if(i)return i},remove(t){delete e[t];},allKeys:()=>Object.keys(e)}}();}}class x{constructor(e,t,i){this.cache=e,this.keyManifest=t,this.nowProvider=i||c;}async setIdToken(e,t,i){var o;const n=this.getIdTokenCacheKey(e);await this.cache.set(n,{id_token:t,decodedToken:i}),await(null===(o=this.keyManifest)||void 0===o?void 0:o.add(n));}async getIdToken(e){const t=await this.cache.get(this.getIdTokenCacheKey(e.clientId));if(!t&&e.scope&&e.audience){const t=await this.get(e);if(!t)return;if(!t.id_token||!t.decodedToken)return;return {id_token:t.id_token,decodedToken:t.decodedToken}}if(t)return {id_token:t.id_token,decodedToken:t.decodedToken}}async get(e,t=0){var i;let o=await this.cache.get(e.toKey());if(!o){const t=await this.getCacheKeys();if(!t)return;const i=this.matchExistingCacheKey(e,t);i&&(o=await this.cache.get(i));}if(!o)return;const n=await this.nowProvider(),a=Math.floor(n/1e3);return o.expiresAt-t<a?o.body.refresh_token?(o.body={refresh_token:o.body.refresh_token},await this.cache.set(e.toKey(),o),o.body):(await this.cache.remove(e.toKey()),void await(null===(i=this.keyManifest)||void 0===i?void 0:i.remove(e.toKey()))):o.body}async set(e){var t;const i=new C({clientId:e.client_id,scope:e.scope,audience:e.audience}),o=await this.wrapCacheEntry(e);await this.cache.set(i.toKey(),o),await(null===(t=this.keyManifest)||void 0===t?void 0:t.add(i.toKey()));}async clear(e){var t;const i=await this.getCacheKeys();i&&(await i.filter((t=>!e||t.includes(e))).reduce((async(e,t)=>{await e,await this.cache.remove(t);}),Promise.resolve()),await(null===(t=this.keyManifest)||void 0===t?void 0:t.clear()));}async wrapCacheEntry(e){const t=await this.nowProvider();return {body:e,expiresAt:Math.floor(t/1e3)+e.expires_in}}async getCacheKeys(){var e;return this.keyManifest?null===(e=await this.keyManifest.get())||void 0===e?void 0:e.keys:this.cache.allKeys?this.cache.allKeys():void 0}getIdTokenCacheKey(e){return new C({clientId:e},"@@auth0spajs@@","@@user@@").toKey()}matchExistingCacheKey(e,t){return t.filter((t=>{var i;const o=C.fromKey(t),n=new Set(o.scope&&o.scope.split(" ")),a=(null===(i=e.scope)||void 0===i?void 0:i.split(" "))||[],r=o.scope&&a.reduce(((e,t)=>e&&n.has(t)),!0);return "@@auth0spajs@@"===o.prefix&&o.clientId===e.clientId&&o.audience===e.audience&&r}))[0]}}class Z{constructor(e,t,i){this.storage=e,this.clientId=t,this.cookieDomain=i,this.storageKey=`a0.spajs.txs.${this.clientId}`;}create(e){this.storage.save(this.storageKey,e,{daysUntilExpire:1,cookieDomain:this.cookieDomain});}get(){return this.storage.get(this.storageKey)}remove(){this.storage.remove(this.storageKey,{cookieDomain:this.cookieDomain});}}const K=e=>"number"==typeof e,W=["iss","aud","exp","nbf","iat","jti","azp","nonce","auth_time","at_hash","c_hash","acr","amr","sub_jwk","cnf","sip_from_tag","sip_date","sip_callid","sip_cseq_num","sip_via_branch","orig","dest","mky","events","toe","txn","rph","sid","vot","vtm"],E=e=>{if(!e.id_token)throw new Error("ID token is required but missing");const t=(e=>{const t=e.split("."),[i,o,n]=t;if(3!==t.length||!i||!o||!n)throw new Error("ID token could not be decoded");const a=JSON.parse(b(o)),r={__raw:e},s={};return Object.keys(a).forEach((e=>{r[e]=a[e],W.includes(e)||(s[e]=a[e]);})),{encoded:{header:i,payload:o,signature:n},header:JSON.parse(b(i)),claims:r,user:s}})(e.id_token);if(!t.claims.iss)throw new Error("Issuer (iss) claim must be a string present in the ID token");if(t.claims.iss!==e.iss)throw new Error(`Issuer (iss) claim mismatch in the ID token; expected "${e.iss}", found "${t.claims.iss}"`);if(!t.user.sub)throw new Error("Subject (sub) claim must be a string present in the ID token");if("RS256"!==t.header.alg)throw new Error(`Signature algorithm of "${t.header.alg}" is not supported. Expected the ID token to be signed with "RS256".`);if(!t.claims.aud||"string"!=typeof t.claims.aud&&!Array.isArray(t.claims.aud))throw new Error("Audience (aud) claim must be a string or array of strings present in the ID token");if(Array.isArray(t.claims.aud)){if(!t.claims.aud.includes(e.aud))throw new Error(`Audience (aud) claim mismatch in the ID token; expected "${e.aud}" but was not one of "${t.claims.aud.join(", ")}"`);if(t.claims.aud.length>1){if(!t.claims.azp)throw new Error("Authorized Party (azp) claim must be a string present in the ID token when Audience (aud) claim has multiple values");if(t.claims.azp!==e.aud)throw new Error(`Authorized Party (azp) claim mismatch in the ID token; expected "${e.aud}", found "${t.claims.azp}"`)}}else if(t.claims.aud!==e.aud)throw new Error(`Audience (aud) claim mismatch in the ID token; expected "${e.aud}" but found "${t.claims.aud}"`);if(e.nonce){if(!t.claims.nonce)throw new Error("Nonce (nonce) claim must be a string present in the ID token");if(t.claims.nonce!==e.nonce)throw new Error(`Nonce (nonce) claim mismatch in the ID token; expected "${e.nonce}", found "${t.claims.nonce}"`)}if(e.max_age&&!K(t.claims.auth_time))throw new Error("Authentication Time (auth_time) claim must be a number present in the ID token when Max Age (max_age) is specified");if(null==t.claims.exp||!K(t.claims.exp))throw new Error("Expiration Time (exp) claim must be a number present in the ID token");if(!K(t.claims.iat))throw new Error("Issued At (iat) claim must be a number present in the ID token");const i=e.leeway||60,o=new Date(e.now||Date.now()),n=new Date(0);if(n.setUTCSeconds(t.claims.exp+i),o>n)throw new Error(`Expiration Time (exp) claim error in the ID token; current time (${o}) is after expiration time (${n})`);if(null!=t.claims.nbf&&K(t.claims.nbf)){const e=new Date(0);if(e.setUTCSeconds(t.claims.nbf-i),o<e)throw new Error(`Not Before time (nbf) claim in the ID token indicates that this token can't be used just yet. Current time (${o}) is before ${e}`)}if(null!=t.claims.auth_time&&K(t.claims.auth_time)){const n=new Date(0);if(n.setUTCSeconds(parseInt(t.claims.auth_time)+e.max_age+i),o>n)throw new Error(`Authentication Time (auth_time) claim in the ID token indicates that too much time has passed since the last end-user authentication. Current time (${o}) is after last auth at ${n}`)}if(e.organization){const i=e.organization.trim();if(i.startsWith("org_")){const e=i;if(!t.claims.org_id)throw new Error("Organization ID (org_id) claim must be a string present in the ID token");if(e!==t.claims.org_id)throw new Error(`Organization ID (org_id) claim mismatch in the ID token; expected "${e}", found "${t.claims.org_id}"`)}else {const e=i.toLowerCase();if(!t.claims.org_name)throw new Error("Organization Name (org_name) claim must be a string present in the ID token");if(e!==t.claims.org_name)throw new Error(`Organization Name (org_name) claim mismatch in the ID token; expected "${e}", found "${t.claims.org_name}"`)}}return t};var R=o((function(e,i){var o=t&&t.__assign||function(){return o=Object.assign||function(e){for(var t,i=1,o=arguments.length;i<o;i++)for(var n in t=arguments[i])Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n]);return e},o.apply(this,arguments)};function n(e,t){if(!t)return "";var i="; "+e;return !0===t?i:i+"="+t}function a(e,t,i){return encodeURIComponent(e).replace(/%(23|24|26|2B|5E|60|7C)/g,decodeURIComponent).replace(/\(/g,"%28").replace(/\)/g,"%29")+"="+encodeURIComponent(t).replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g,decodeURIComponent)+function(e){if("number"==typeof e.expires){var t=new Date;t.setMilliseconds(t.getMilliseconds()+864e5*e.expires),e.expires=t;}return n("Expires",e.expires?e.expires.toUTCString():"")+n("Domain",e.domain)+n("Path",e.path)+n("Secure",e.secure)+n("SameSite",e.sameSite)}(i)}function r(e){for(var t={},i=e?e.split("; "):[],o=/(%[\dA-F]{2})+/gi,n=0;n<i.length;n++){var a=i[n].split("="),r=a.slice(1).join("=");'"'===r.charAt(0)&&(r=r.slice(1,-1));try{t[a[0].replace(o,decodeURIComponent)]=r.replace(o,decodeURIComponent);}catch(e){}}return t}function s(){return r(document.cookie)}function c(e,t,i){document.cookie=a(e,t,o({path:"/"},i));}i.__esModule=!0,i.encode=a,i.parse=r,i.getAll=s,i.get=function(e){return s()[e]},i.set=c,i.remove=function(e,t){c(e,"",o(o({},t),{expires:-1}));};}));i(R),R.encode,R.parse,R.getAll;var U=R.get,L=R.set,D=R.remove;const X={get(e){const t=U(e);if(void 0!==t)return JSON.parse(t)},save(e,t,i){let o={};"https:"===window.location.protocol&&(o={secure:!0,sameSite:"none"}),(null==i?void 0:i.daysUntilExpire)&&(o.expires=i.daysUntilExpire),(null==i?void 0:i.cookieDomain)&&(o.domain=i.cookieDomain),L(e,JSON.stringify(t),o);},remove(e,t){let i={};(null==t?void 0:t.cookieDomain)&&(i.domain=t.cookieDomain),D(e,i);}},N={get(e){const t=X.get(e);return t||X.get(`_legacy_${e}`)},save(e,t,i){let o={};"https:"===window.location.protocol&&(o={secure:!0}),(null==i?void 0:i.daysUntilExpire)&&(o.expires=i.daysUntilExpire),(null==i?void 0:i.cookieDomain)&&(o.domain=i.cookieDomain),L(`_legacy_${e}`,JSON.stringify(t),o),X.save(e,t,i);},remove(e,t){let i={};(null==t?void 0:t.cookieDomain)&&(i.domain=t.cookieDomain),D(e,i),X.remove(e,t),X.remove(`_legacy_${e}`,t);}},J={get(e){if("undefined"==typeof sessionStorage)return;const t=sessionStorage.getItem(e);return null!=t?JSON.parse(t):void 0},save(e,t){sessionStorage.setItem(e,JSON.stringify(t));},remove(e){sessionStorage.removeItem(e);}};function F(e,t,i){var o=void 0===t?null:t,n=function(e,t){var i=atob(e);if(t){for(var o=new Uint8Array(i.length),n=0,a=i.length;n<a;++n)o[n]=i.charCodeAt(n);return String.fromCharCode.apply(null,new Uint16Array(o.buffer))}return i}(e,void 0!==i&&i),a=n.indexOf("\n",10)+1,r=n.substring(a)+(o?"//# sourceMappingURL="+o:""),s=new Blob([r],{type:"application/javascript"});return URL.createObjectURL(s)}var H,Y,G,V,M=(H="Lyogcm9sbHVwLXBsdWdpbi13ZWItd29ya2VyLWxvYWRlciAqLwohZnVuY3Rpb24oKXsidXNlIHN0cmljdCI7Y2xhc3MgZSBleHRlbmRzIEVycm9ye2NvbnN0cnVjdG9yKHQscil7c3VwZXIociksdGhpcy5lcnJvcj10LHRoaXMuZXJyb3JfZGVzY3JpcHRpb249cixPYmplY3Quc2V0UHJvdG90eXBlT2YodGhpcyxlLnByb3RvdHlwZSl9c3RhdGljIGZyb21QYXlsb2FkKHtlcnJvcjp0LGVycm9yX2Rlc2NyaXB0aW9uOnJ9KXtyZXR1cm4gbmV3IGUodCxyKX19Y2xhc3MgdCBleHRlbmRzIGV7Y29uc3RydWN0b3IoZSxzKXtzdXBlcigibWlzc2luZ19yZWZyZXNoX3Rva2VuIixgTWlzc2luZyBSZWZyZXNoIFRva2VuIChhdWRpZW5jZTogJyR7cihlLFsiZGVmYXVsdCJdKX0nLCBzY29wZTogJyR7cihzKX0nKWApLHRoaXMuYXVkaWVuY2U9ZSx0aGlzLnNjb3BlPXMsT2JqZWN0LnNldFByb3RvdHlwZU9mKHRoaXMsdC5wcm90b3R5cGUpfX1mdW5jdGlvbiByKGUsdD1bXSl7cmV0dXJuIGUmJiF0LmluY2x1ZGVzKGUpP2U6IiJ9ImZ1bmN0aW9uIj09dHlwZW9mIFN1cHByZXNzZWRFcnJvciYmU3VwcHJlc3NlZEVycm9yO2NvbnN0IHM9ZT0+e3ZhcntjbGllbnRJZDp0fT1lLHI9ZnVuY3Rpb24oZSx0KXt2YXIgcj17fTtmb3IodmFyIHMgaW4gZSlPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwoZSxzKSYmdC5pbmRleE9mKHMpPDAmJihyW3NdPWVbc10pO2lmKG51bGwhPWUmJiJmdW5jdGlvbiI9PXR5cGVvZiBPYmplY3QuZ2V0T3duUHJvcGVydHlTeW1ib2xzKXt2YXIgbz0wO2ZvcihzPU9iamVjdC5nZXRPd25Qcm9wZXJ0eVN5bWJvbHMoZSk7bzxzLmxlbmd0aDtvKyspdC5pbmRleE9mKHNbb10pPDAmJk9iamVjdC5wcm90b3R5cGUucHJvcGVydHlJc0VudW1lcmFibGUuY2FsbChlLHNbb10pJiYocltzW29dXT1lW3Nbb11dKX1yZXR1cm4gcn0oZSxbImNsaWVudElkIl0pO3JldHVybiBuZXcgVVJMU2VhcmNoUGFyYW1zKChlPT5PYmplY3Qua2V5cyhlKS5maWx0ZXIoKHQ9PnZvaWQgMCE9PWVbdF0pKS5yZWR1Y2UoKCh0LHIpPT5PYmplY3QuYXNzaWduKE9iamVjdC5hc3NpZ24oe30sdCkse1tyXTplW3JdfSkpLHt9KSkoT2JqZWN0LmFzc2lnbih7Y2xpZW50X2lkOnR9LHIpKSkudG9TdHJpbmcoKX07bGV0IG89e307Y29uc3Qgbj0oZSx0KT0+YCR7ZX18JHt0fWA7YWRkRXZlbnRMaXN0ZW5lcigibWVzc2FnZSIsKGFzeW5jKHtkYXRhOnt0aW1lb3V0OmUsYXV0aDpyLGZldGNoVXJsOmksZmV0Y2hPcHRpb25zOmMsdXNlRm9ybURhdGE6YX0scG9ydHM6W3BdfSk9PntsZXQgZjtjb25zdHthdWRpZW5jZTp1LHNjb3BlOmx9PXJ8fHt9O3RyeXtjb25zdCByPWE/KGU9Pntjb25zdCB0PW5ldyBVUkxTZWFyY2hQYXJhbXMoZSkscj17fTtyZXR1cm4gdC5mb3JFYWNoKCgoZSx0KT0+e3JbdF09ZX0pKSxyfSkoYy5ib2R5KTpKU09OLnBhcnNlKGMuYm9keSk7aWYoIXIucmVmcmVzaF90b2tlbiYmInJlZnJlc2hfdG9rZW4iPT09ci5ncmFudF90eXBlKXtjb25zdCBlPSgoZSx0KT0+b1tuKGUsdCldKSh1LGwpO2lmKCFlKXRocm93IG5ldyB0KHUsbCk7Yy5ib2R5PWE/cyhPYmplY3QuYXNzaWduKE9iamVjdC5hc3NpZ24oe30scikse3JlZnJlc2hfdG9rZW46ZX0pKTpKU09OLnN0cmluZ2lmeShPYmplY3QuYXNzaWduKE9iamVjdC5hc3NpZ24oe30scikse3JlZnJlc2hfdG9rZW46ZX0pKX1sZXQgaCxnOyJmdW5jdGlvbiI9PXR5cGVvZiBBYm9ydENvbnRyb2xsZXImJihoPW5ldyBBYm9ydENvbnRyb2xsZXIsYy5zaWduYWw9aC5zaWduYWwpO3RyeXtnPWF3YWl0IFByb21pc2UucmFjZShbKGQ9ZSxuZXcgUHJvbWlzZSgoZT0+c2V0VGltZW91dChlLGQpKSkpLGZldGNoKGksT2JqZWN0LmFzc2lnbih7fSxjKSldKX1jYXRjaChlKXtyZXR1cm4gdm9pZCBwLnBvc3RNZXNzYWdlKHtlcnJvcjplLm1lc3NhZ2V9KX1pZighZylyZXR1cm4gaCYmaC5hYm9ydCgpLHZvaWQgcC5wb3N0TWVzc2FnZSh7ZXJyb3I6IlRpbWVvdXQgd2hlbiBleGVjdXRpbmcgJ2ZldGNoJyJ9KTtmPWF3YWl0IGcuanNvbigpLGYucmVmcmVzaF90b2tlbj8oKChlLHQscik9PntvW24odCxyKV09ZX0pKGYucmVmcmVzaF90b2tlbix1LGwpLGRlbGV0ZSBmLnJlZnJlc2hfdG9rZW4pOigoZSx0KT0+e2RlbGV0ZSBvW24oZSx0KV19KSh1LGwpLHAucG9zdE1lc3NhZ2Uoe29rOmcub2ssanNvbjpmfSl9Y2F0Y2goZSl7cC5wb3N0TWVzc2FnZSh7b2s6ITEsanNvbjp7ZXJyb3I6ZS5lcnJvcixlcnJvcl9kZXNjcmlwdGlvbjplLm1lc3NhZ2V9fSl9dmFyIGR9KSl9KCk7Cgo=",Y=null,G=!1,function(e){return V=V||F(H,Y,G),new Worker(V,e)});const A={};class B{constructor(e,t){this.cache=e,this.clientId=t,this.manifestKey=this.createManifestKeyFrom(this.clientId);}async add(e){var t;const i=new Set((null===(t=await this.cache.get(this.manifestKey))||void 0===t?void 0:t.keys)||[]);i.add(e),await this.cache.set(this.manifestKey,{keys:[...i]});}async remove(e){const t=await this.cache.get(this.manifestKey);if(t){const i=new Set(t.keys);return i.delete(e),i.size>0?await this.cache.set(this.manifestKey,{keys:[...i]}):await this.cache.remove(this.manifestKey)}}get(){return this.cache.get(this.manifestKey)}clear(){return this.cache.remove(this.manifestKey)}createManifestKeyFrom(e){return `@@auth0spajs@@::${e}`}}const $={memory:()=>(new P).enclosedCache,localstorage:()=>new z},q=e=>$[e],Q=t=>{const{openUrl:i,onRedirect:o}=t,n=e(t,["openUrl","onRedirect"]);return Object.assign(Object.assign({},n),{openUrl:!1===i||i?i:o})},ee=new a;class te{constructor(e){let t,i;if(this.userCache=(new P).enclosedCache,this.defaultOptions={authorizationParams:{scope:"openid profile email"},useRefreshTokensFallback:!1,useFormData:!0},this._releaseLockOnPageHide=async()=>{await ee.releaseLock("auth0.lock.getTokenSilently"),window.removeEventListener("pagehide",this._releaseLockOnPageHide);},this.options=Object.assign(Object.assign(Object.assign({},this.defaultOptions),e),{authorizationParams:Object.assign(Object.assign({},this.defaultOptions.authorizationParams),e.authorizationParams)}),"undefined"!=typeof window&&(()=>{if(!w())throw new Error("For security reasons, `window.crypto` is required to run `auth0-spa-js`.");if(void 0===w().subtle)throw new Error("\n      auth0-spa-js must run on a secure origin. See https://github.com/auth0/auth0-spa-js/blob/main/FAQ.md#why-do-i-get-auth0-spa-js-must-run-on-a-secure-origin for more information.\n    ")})(),e.cache&&e.cacheLocation&&console.warn("Both `cache` and `cacheLocation` options have been specified in the Auth0Client configuration; ignoring `cacheLocation` and using `cache`."),e.cache)i=e.cache;else {if(t=e.cacheLocation||"memory",!q(t))throw new Error(`Invalid cache location "${t}"`);i=q(t)();}this.httpTimeoutMs=e.httpTimeoutInSeconds?1e3*e.httpTimeoutInSeconds:1e4,this.cookieStorage=!1===e.legacySameSiteCookie?X:N,this.orgHintCookieName=`auth0.${this.options.clientId}.organization_hint`,this.isAuthenticatedCookieName=(e=>`auth0.${e}.is.authenticated`)(this.options.clientId),this.sessionCheckExpiryDays=e.sessionCheckExpiryDays||1;const o=e.useCookiesForTransactions?this.cookieStorage:J;var n;this.scope=j("openid",this.options.authorizationParams.scope,this.options.useRefreshTokens?"offline_access":""),this.transactionManager=new Z(o,this.options.clientId,this.options.cookieDomain),this.nowProvider=this.options.nowProvider||c,this.cacheManager=new x(i,i.allKeys?void 0:new B(i,this.options.clientId),this.nowProvider),this.domainUrl=(n=this.options.domain,/^https?:\/\//.test(n)?n:`https://${n}`),this.tokenIssuer=((e,t)=>e?e.startsWith("https://")?e:`https://${e}/`:`${t}/`)(this.options.issuer,this.domainUrl),"undefined"!=typeof window&&window.Worker&&this.options.useRefreshTokens&&"memory"===t&&(this.options.workerUrl?this.worker=new Worker(this.options.workerUrl):this.worker=new M);}_url(e){const t=encodeURIComponent(btoa(JSON.stringify(this.options.auth0Client||s)));return `${this.domainUrl}${e}&auth0Client=${t}`}_authorizeUrl(e){return this._url(`/authorize?${v(e)}`)}async _verifyIdToken(e,t,i){const o=await this.nowProvider();return E({iss:this.tokenIssuer,aud:this.options.clientId,id_token:e,nonce:t,organization:i,leeway:this.options.leeway,max_age:(n=this.options.authorizationParams.max_age,"string"!=typeof n?n:parseInt(n,10)||void 0),now:o});var n;}_processOrgHint(e){e?this.cookieStorage.save(this.orgHintCookieName,e,{daysUntilExpire:this.sessionCheckExpiryDays,cookieDomain:this.options.cookieDomain}):this.cookieStorage.remove(this.orgHintCookieName,{cookieDomain:this.options.cookieDomain});}async _prepareAuthorizeUrl(e,t,i){const o=k(y()),n=k(y()),a=y(),r=(e=>{const t=new Uint8Array(e);return (e=>{const t={"+":"-","/":"_","=":""};return e.replace(/[+/=]/g,(e=>t[e]))})(window.btoa(String.fromCharCode(...Array.from(t))))})(await(async e=>{const t=w().subtle.digest({name:"SHA-256"},(new TextEncoder).encode(e));return await t})(a)),s=((e,t,i,o,n,a,r,s)=>Object.assign(Object.assign(Object.assign({client_id:e.clientId},e.authorizationParams),i),{scope:j(t,i.scope),response_type:"code",response_mode:s||"query",state:o,nonce:n,redirect_uri:r||e.authorizationParams.redirect_uri,code_challenge:a,code_challenge_method:"S256"}))(this.options,this.scope,e,o,n,r,e.redirect_uri||this.options.authorizationParams.redirect_uri||i,null==t?void 0:t.response_mode),c=this._authorizeUrl(s);return {nonce:n,code_verifier:a,scope:s.scope,audience:s.audience||"default",redirect_uri:s.redirect_uri,state:o,url:c}}async loginWithPopup(e,t){var i;if(e=e||{},!(t=t||{}).popup&&(t.popup=(e=>{const t=window.screenX+(window.innerWidth-400)/2,i=window.screenY+(window.innerHeight-600)/2;return window.open(e,"auth0:authorize:popup",`left=${t},top=${i},width=400,height=600,resizable,scrollbars=yes,status=1`)})(""),!t.popup))throw new Error("Unable to open a popup for loginWithPopup - window.open returned `null`");const o=await this._prepareAuthorizeUrl(e.authorizationParams||{},{response_mode:"web_message"},window.location.origin);t.popup.location.href=o.url;const n=await(e=>new Promise(((t,i)=>{let o;const n=setInterval((()=>{e.popup&&e.popup.closed&&(clearInterval(n),clearTimeout(a),window.removeEventListener("message",o,!1),i(new p(e.popup)));}),1e3),a=setTimeout((()=>{clearInterval(n),i(new h(e.popup)),window.removeEventListener("message",o,!1);}),1e3*(e.timeoutInSeconds||60));o=function(r){if(r.data&&"authorization_response"===r.data.type){if(clearTimeout(a),clearInterval(n),window.removeEventListener("message",o,!1),e.popup.close(),r.data.response.error)return i(d.fromPayload(r.data.response));t(r.data.response);}},window.addEventListener("message",o);})))(Object.assign(Object.assign({},t),{timeoutInSeconds:t.timeoutInSeconds||this.options.authorizeTimeoutInSeconds||60}));if(o.state!==n.state)throw new d("state_mismatch","Invalid state");const a=(null===(i=e.authorizationParams)||void 0===i?void 0:i.organization)||this.options.authorizationParams.organization;await this._requestToken({audience:o.audience,scope:o.scope,code_verifier:o.code_verifier,grant_type:"authorization_code",code:n.code,redirect_uri:o.redirect_uri},{nonceIn:o.nonce,organization:a});}async getUser(){var e;const t=await this._getIdTokenFromCache();return null===(e=null==t?void 0:t.decodedToken)||void 0===e?void 0:e.user}async getIdTokenClaims(){var e;const t=await this._getIdTokenFromCache();return null===(e=null==t?void 0:t.decodedToken)||void 0===e?void 0:e.claims}async loginWithRedirect(t={}){var i;const o=Q(t),{openUrl:n,fragment:a,appState:r}=o,s=e(o,["openUrl","fragment","appState"]),c=(null===(i=s.authorizationParams)||void 0===i?void 0:i.organization)||this.options.authorizationParams.organization,d=await this._prepareAuthorizeUrl(s.authorizationParams||{}),{url:u}=d,l=e(d,["url"]);this.transactionManager.create(Object.assign(Object.assign(Object.assign({},l),{appState:r}),c&&{organization:c}));const h=a?`${u}#${a}`:u;n?await n(h):window.location.assign(h);}async handleRedirectCallback(e=window.location.href){const t=e.split("?").slice(1);if(0===t.length)throw new Error("There are no query params available for parsing.");const{state:i,code:o,error:n,error_description:a}=(e=>{e.indexOf("#")>-1&&(e=e.substring(0,e.indexOf("#")));const t=new URLSearchParams(e);return {state:t.get("state"),code:t.get("code")||void 0,error:t.get("error")||void 0,error_description:t.get("error_description")||void 0}})(t.join("")),r=this.transactionManager.get();if(!r)throw new d("missing_transaction","Invalid state");if(this.transactionManager.remove(),n)throw new u(n,a||n,i,r.appState);if(!r.code_verifier||r.state&&r.state!==i)throw new d("state_mismatch","Invalid state");const s=r.organization,c=r.nonce,l=r.redirect_uri;return await this._requestToken(Object.assign({audience:r.audience,scope:r.scope,code_verifier:r.code_verifier,grant_type:"authorization_code",code:o},l?{redirect_uri:l}:{}),{nonceIn:c,organization:s}),{appState:r.appState}}async checkSession(e){if(!this.cookieStorage.get(this.isAuthenticatedCookieName)){if(!this.cookieStorage.get("auth0.is.authenticated"))return;this.cookieStorage.save(this.isAuthenticatedCookieName,!0,{daysUntilExpire:this.sessionCheckExpiryDays,cookieDomain:this.options.cookieDomain}),this.cookieStorage.remove("auth0.is.authenticated");}try{await this.getTokenSilently(e);}catch(e){}}async getTokenSilently(e={}){var t;const i=Object.assign(Object.assign({cacheMode:"on"},e),{authorizationParams:Object.assign(Object.assign(Object.assign({},this.options.authorizationParams),e.authorizationParams),{scope:j(this.scope,null===(t=e.authorizationParams)||void 0===t?void 0:t.scope)})}),o=await((e,t)=>{let i=A[t];return i||(i=e().finally((()=>{delete A[t],i=null;})),A[t]=i),i})((()=>this._getTokenSilently(i)),`${this.options.clientId}::${i.authorizationParams.audience}::${i.authorizationParams.scope}`);return e.detailedResponse?o:null==o?void 0:o.access_token}async _getTokenSilently(t){const{cacheMode:i}=t,o=e(t,["cacheMode"]);if("off"!==i){const e=await this._getEntryFromCache({scope:o.authorizationParams.scope,audience:o.authorizationParams.audience||"default",clientId:this.options.clientId});if(e)return e}if("cache-only"!==i){if(!await(async(e,t=3)=>{for(let i=0;i<t;i++)if(await e())return !0;return !1})((()=>ee.acquireLock("auth0.lock.getTokenSilently",5e3)),10))throw new l;try{if(window.addEventListener("pagehide",this._releaseLockOnPageHide),"off"!==i){const e=await this._getEntryFromCache({scope:o.authorizationParams.scope,audience:o.authorizationParams.audience||"default",clientId:this.options.clientId});if(e)return e}const e=this.options.useRefreshTokens?await this._getTokenUsingRefreshToken(o):await this._getTokenFromIFrame(o),{id_token:t,access_token:n,oauthTokenScope:a,expires_in:r}=e;return Object.assign(Object.assign({id_token:t,access_token:n},a?{scope:a}:null),{expires_in:r})}finally{await ee.releaseLock("auth0.lock.getTokenSilently"),window.removeEventListener("pagehide",this._releaseLockOnPageHide);}}}async getTokenWithPopup(e={},t={}){var i;const o=Object.assign(Object.assign({},e),{authorizationParams:Object.assign(Object.assign(Object.assign({},this.options.authorizationParams),e.authorizationParams),{scope:j(this.scope,null===(i=e.authorizationParams)||void 0===i?void 0:i.scope)})});t=Object.assign(Object.assign({},r),t),await this.loginWithPopup(o,t);return (await this.cacheManager.get(new C({scope:o.authorizationParams.scope,audience:o.authorizationParams.audience||"default",clientId:this.options.clientId}))).access_token}async isAuthenticated(){return !!await this.getUser()}_buildLogoutUrl(t){null!==t.clientId?t.clientId=t.clientId||this.options.clientId:delete t.clientId;const i=t.logoutParams||{},{federated:o}=i,n=e(i,["federated"]),a=o?"&federated":"";return this._url(`/v2/logout?${v(Object.assign({clientId:t.clientId},n))}`)+a}async logout(t={}){const i=Q(t),{openUrl:o}=i,n=e(i,["openUrl"]);null===t.clientId?await this.cacheManager.clear():await this.cacheManager.clear(t.clientId||this.options.clientId),this.cookieStorage.remove(this.orgHintCookieName,{cookieDomain:this.options.cookieDomain}),this.cookieStorage.remove(this.isAuthenticatedCookieName,{cookieDomain:this.options.cookieDomain}),this.userCache.remove("@@user@@");const a=this._buildLogoutUrl(n);o?await o(a):!1!==o&&window.location.assign(a);}async _getTokenFromIFrame(e){const t=Object.assign(Object.assign({},e.authorizationParams),{prompt:"none"}),i=this.cookieStorage.get(this.orgHintCookieName);i&&!t.organization&&(t.organization=i);const{url:o,state:n,nonce:a,code_verifier:r,redirect_uri:s,scope:c,audience:u}=await this._prepareAuthorizeUrl(t,{response_mode:"web_message"},window.location.origin);try{if(window.crossOriginIsolated)throw new d("login_required","The application is running in a Cross-Origin Isolated context, silently retrieving a token without refresh token is not possible.");const i=e.timeoutInSeconds||this.options.authorizeTimeoutInSeconds,h=await((e,t,i=60)=>new Promise(((o,n)=>{const a=window.document.createElement("iframe");a.setAttribute("width","0"),a.setAttribute("height","0"),a.style.display="none";const r=()=>{window.document.body.contains(a)&&(window.document.body.removeChild(a),window.removeEventListener("message",s,!1));};let s;const c=setTimeout((()=>{n(new l),r();}),1e3*i);s=function(e){if(e.origin!=t)return;if(!e.data||"authorization_response"!==e.data.type)return;const i=e.source;i&&i.close(),e.data.response.error?n(d.fromPayload(e.data.response)):o(e.data.response),clearTimeout(c),window.removeEventListener("message",s,!1),setTimeout(r,2e3);},window.addEventListener("message",s,!1),window.document.body.appendChild(a),a.setAttribute("src",e);})))(o,this.domainUrl,i);if(n!==h.state)throw new d("state_mismatch","Invalid state");const p=await this._requestToken(Object.assign(Object.assign({},e.authorizationParams),{code_verifier:r,code:h.code,grant_type:"authorization_code",redirect_uri:s,timeout:e.authorizationParams.timeout||this.httpTimeoutMs}),{nonceIn:a,organization:t.organization});return Object.assign(Object.assign({},p),{scope:c,oauthTokenScope:p.scope,audience:u})}catch(e){throw "login_required"===e.error&&this.logout({openUrl:!1}),e}}async _getTokenUsingRefreshToken(e){const t=await this.cacheManager.get(new C({scope:e.authorizationParams.scope,audience:e.authorizationParams.audience||"default",clientId:this.options.clientId}));if(!(t&&t.refresh_token||this.worker)){if(this.options.useRefreshTokensFallback)return await this._getTokenFromIFrame(e);throw new f(e.authorizationParams.audience||"default",e.authorizationParams.scope)}const i=e.authorizationParams.redirect_uri||this.options.authorizationParams.redirect_uri||window.location.origin,o="number"==typeof e.timeoutInSeconds?1e3*e.timeoutInSeconds:null;try{const n=await this._requestToken(Object.assign(Object.assign(Object.assign({},e.authorizationParams),{grant_type:"refresh_token",refresh_token:t&&t.refresh_token,redirect_uri:i}),o&&{timeout:o}));return Object.assign(Object.assign({},n),{scope:e.authorizationParams.scope,oauthTokenScope:n.scope,audience:e.authorizationParams.audience||"default"})}catch(t){if((t.message.indexOf("Missing Refresh Token")>-1||t.message&&t.message.indexOf("invalid refresh token")>-1)&&this.options.useRefreshTokensFallback)return await this._getTokenFromIFrame(e);throw t}}async _saveEntryInCache(t){const{id_token:i,decodedToken:o}=t,n=e(t,["id_token","decodedToken"]);this.userCache.set("@@user@@",{id_token:i,decodedToken:o}),await this.cacheManager.setIdToken(this.options.clientId,t.id_token,t.decodedToken),await this.cacheManager.set(n);}async _getIdTokenFromCache(){const e=this.options.authorizationParams.audience||"default",t=await this.cacheManager.getIdToken(new C({clientId:this.options.clientId,audience:e,scope:this.scope})),i=this.userCache.get("@@user@@");return t&&t.id_token===(null==i?void 0:i.id_token)?i:(this.userCache.set("@@user@@",t),t)}async _getEntryFromCache({scope:e,audience:t,clientId:i}){const o=await this.cacheManager.get(new C({scope:e,audience:t,clientId:i}),60);if(o&&o.access_token){const{access_token:e,oauthTokenScope:t,expires_in:i}=o,n=await this._getIdTokenFromCache();return n&&Object.assign(Object.assign({id_token:n.id_token,access_token:e},t?{scope:t}:null),{expires_in:i})}}async _requestToken(e,t){const{nonceIn:i,organization:o}=t||{},n=await T(Object.assign({baseUrl:this.domainUrl,client_id:this.options.clientId,auth0Client:this.options.auth0Client,useFormData:this.options.useFormData,timeout:this.httpTimeoutMs},e),this.worker),a=await this._verifyIdToken(n.id_token,i,o);return await this._saveEntryInCache(Object.assign(Object.assign(Object.assign(Object.assign({},n),{decodedToken:a,scope:e.scope,audience:e.audience||"default"}),n.scope?{oauthTokenScope:n.scope}:null),{client_id:this.options.clientId})),this.cookieStorage.save(this.isAuthenticatedCookieName,!0,{daysUntilExpire:this.sessionCheckExpiryDays,cookieDomain:this.options.cookieDomain}),this._processOrgHint(o||a.claims.org_id),Object.assign(Object.assign({},n),{decodedToken:a})}}class ie{}

  /* eslint-disable @typescript-eslint/no-explicit-any */
  /**
   * @ignore
   * Run watchEffect untill the watcher returns true, then stop the watch.
   * Once it returns true, the promise will resolve.
   */
  function watchEffectOnceAsync(watcher) {
      return new Promise(resolve => {
          watchEffectOnce(watcher, resolve);
      });
  }
  /**
   * @ignore
   * Run watchEffect untill the watcher returns true, then stop the watch.
   * Once it returns true, it will call the provided function.
   */
  function watchEffectOnce(watcher, fn) {
      const stopWatch = vue.watchEffect(() => {
          if (watcher()) {
              fn();
              stopWatch();
          }
      });
  }
  /**
   * @ignore
   * Helper function to bind methods to itself, useful when using Vue's `provide` / `inject` API's.
   */
  function bindPluginMethods(plugin, exclude) {
      Object.getOwnPropertyNames(Object.getPrototypeOf(plugin))
          .filter(method => !exclude.includes(method))
          // eslint-disable-next-line security/detect-object-injection
          .forEach(method => (plugin[method] = plugin[method].bind(plugin)));
  }
  /**
   * @ignore
   * Helper function to map the v1 `redirect_uri` option to the v2 `authorizationParams.redirect_uri`
   * and log a warning.
   */
  function deprecateRedirectUri(options) {
      if (options === null || options === void 0 ? void 0 : options.redirect_uri) {
          console.warn('Using `redirect_uri` has been deprecated, please use `authorizationParams.redirect_uri` instead as `redirectUri` will be no longer supported in a future version');
          options.authorizationParams = options.authorizationParams || {};
          options.authorizationParams.redirect_uri = options.redirect_uri;
          delete options.redirect_uri;
      }
  }

  /**
   * Helper callback that's used by default before the plugin is installed.
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const PLUGIN_NOT_INSTALLED_HANDLER = () => {
      console.error(`Please ensure Auth0's Vue plugin is correctly installed.`);
  };
  /**
   * Helper client that's used by default before the plugin is installed.
   */
  const PLUGIN_NOT_INSTALLED_CLIENT = {
      isLoading: vue.ref(false),
      isAuthenticated: vue.ref(false),
      user: vue.ref(undefined),
      idTokenClaims: vue.ref(undefined),
      error: vue.ref(null),
      loginWithPopup: PLUGIN_NOT_INSTALLED_HANDLER,
      loginWithRedirect: PLUGIN_NOT_INSTALLED_HANDLER,
      getAccessTokenSilently: PLUGIN_NOT_INSTALLED_HANDLER,
      getAccessTokenWithPopup: PLUGIN_NOT_INSTALLED_HANDLER,
      logout: PLUGIN_NOT_INSTALLED_HANDLER,
      checkSession: PLUGIN_NOT_INSTALLED_HANDLER,
      handleRedirectCallback: PLUGIN_NOT_INSTALLED_HANDLER
  };
  /**
   * @ignore
   */
  const client = vue.ref(
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  PLUGIN_NOT_INSTALLED_CLIENT);
  /**
   * @ignore
   */
  class Auth0Plugin {
      constructor(clientOptions, pluginOptions) {
          this.clientOptions = clientOptions;
          this.pluginOptions = pluginOptions;
          this.isLoading = vue.ref(true);
          this.isAuthenticated = vue.ref(false);
          this.user = vue.ref({});
          this.idTokenClaims = vue.ref();
          this.error = vue.ref(null);
          // Vue Plugins can have issues when passing around the instance to `provide`
          // Therefor we need to bind all methods correctly to `this`.
          bindPluginMethods(this, ['constructor']);
      }
      install(app) {
          this._client = new te(Object.assign(Object.assign({}, this.clientOptions), { auth0Client: {
                  name: 'auth0-vue',
                  version: version
              } }));
          this.__checkSession(app.config.globalProperties.$router);
          // eslint-disable-next-line security/detect-object-injection
          app.config.globalProperties[AUTH0_TOKEN] = this;
          app.provide(AUTH0_INJECTION_KEY, this);
          client.value = this;
      }
      async loginWithRedirect(options) {
          deprecateRedirectUri(options);
          return this._client.loginWithRedirect(options);
      }
      async loginWithPopup(options, config) {
          deprecateRedirectUri(options);
          return this.__proxy(() => this._client.loginWithPopup(options, config));
      }
      async logout(options) {
          if ((options === null || options === void 0 ? void 0 : options.openUrl) || (options === null || options === void 0 ? void 0 : options.openUrl) === false) {
              return this.__proxy(() => this._client.logout(options));
          }
          return this._client.logout(options);
      }
      /* istanbul ignore next */
      async getAccessTokenSilently(options = {}) {
          deprecateRedirectUri(options);
          return this.__proxy(() => this._client.getTokenSilently(options));
      }
      async getAccessTokenWithPopup(options, config) {
          deprecateRedirectUri(options);
          return this.__proxy(() => this._client.getTokenWithPopup(options, config));
      }
      async checkSession(options) {
          return this.__proxy(() => this._client.checkSession(options));
      }
      async handleRedirectCallback(url) {
          return this.__proxy(() => this._client.handleRedirectCallback(url));
      }
      async __checkSession(router) {
          var _a, _b, _c;
          const search = window.location.search;
          try {
              if ((search.includes('code=') || search.includes('error=')) &&
                  search.includes('state=') &&
                  !((_a = this.pluginOptions) === null || _a === void 0 ? void 0 : _a.skipRedirectCallback)) {
                  const result = await this.handleRedirectCallback();
                  const appState = result === null || result === void 0 ? void 0 : result.appState;
                  const target = (_b = appState === null || appState === void 0 ? void 0 : appState.target) !== null && _b !== void 0 ? _b : '/';
                  window.history.replaceState({}, '', '/');
                  if (router) {
                      router.push(target);
                  }
                  return result;
              }
              else {
                  await this.checkSession();
              }
          }
          catch (e) {
              // __checkSession should never throw an exception as it will fail installing the plugin.
              // Instead, errors during __checkSession are propagated using the errors property on `useAuth0`.
              window.history.replaceState({}, '', '/');
              if (router) {
                  router.push(((_c = this.pluginOptions) === null || _c === void 0 ? void 0 : _c.errorPath) || '/');
              }
          }
      }
      async __refreshState() {
          this.isAuthenticated.value = await this._client.isAuthenticated();
          this.user.value = await this._client.getUser();
          this.idTokenClaims.value = await this._client.getIdTokenClaims();
          this.isLoading.value = false;
      }
      async __proxy(cb, refreshState = true) {
          let result;
          try {
              result = await cb();
              this.error.value = null;
          }
          catch (e) {
              this.error.value = e;
              throw e;
          }
          finally {
              if (refreshState) {
                  await this.__refreshState();
              }
          }
          return result;
      }
  }

  async function createGuardHandler(client, to, redirectLoginOptions) {
      const fn = async () => {
          if (vue.unref(client.isAuthenticated)) {
              return true;
          }
          await client.loginWithRedirect(Object.assign({ appState: { target: to.fullPath } }, redirectLoginOptions));
          return false;
      };
      if (!vue.unref(client.isLoading)) {
          return fn();
      }
      await watchEffectOnceAsync(() => !vue.unref(client.isLoading));
      return fn();
  }
  function createAuthGuard(appOrOptions) {
      const { app, redirectLoginOptions } = !appOrOptions || 'config' in appOrOptions
          ? { app: appOrOptions, redirectLoginOptions: undefined }
          : appOrOptions;
      return async (to) => {
          // eslint-disable-next-line security/detect-object-injection
          const auth0 = app
              ? app.config.globalProperties[AUTH0_TOKEN]
              : vue.unref(client);
          return createGuardHandler(auth0, to, redirectLoginOptions);
      };
  }
  async function authGuard(to) {
      const auth0 = vue.unref(client);
      return createGuardHandler(auth0, to);
  }

  /**
   * Creates the Auth0 plugin.
   *
   * @param clientOptions The Auth Vue Client Options
   * @param pluginOptions Additional Plugin Configuration Options
   * @returns An instance of Auth0Plugin
   */
  function createAuth0(clientOptions, pluginOptions) {
      deprecateRedirectUri(clientOptions);
      return new Auth0Plugin(clientOptions, pluginOptions);
  }
  /**
   * Returns the registered Auth0 instance using Vue's `inject`.
   * @returns An instance of Auth0VueClient
   */
  function useAuth0() {
      return vue.inject(AUTH0_INJECTION_KEY);
  }

  var Auth0Vue = /*#__PURE__*/Object.freeze({
    __proto__: null,
    createAuth0: createAuth0,
    useAuth0: useAuth0,
    AUTH0_INJECTION_KEY: AUTH0_INJECTION_KEY,
    Auth0Plugin: Auth0Plugin,
    User: ie,
    InMemoryCache: P,
    LocalStorageCache: z,
    createAuthGuard: createAuthGuard,
    authGuard: authGuard
  });

  return Auth0Vue;

}));
('Auth0Client' in this) && this.console && this.console.warn && this.console.warn('Auth0Client already declared on the global namespace');
this && this.vueAuth0 && (this.Auth0Client = this.Auth0Client || this.vueAuth0.Auth0Client);
//# sourceMappingURL=auth0-vue.development.js.map
