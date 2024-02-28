'use strict';

var vue = require('vue');
var auth0SpaJs = require('@auth0/auth0-spa-js');

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
        this._client = new auth0SpaJs.Auth0Client(Object.assign(Object.assign({}, this.clientOptions), { auth0Client: {
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
  User: auth0SpaJs.User,
  InMemoryCache: auth0SpaJs.InMemoryCache,
  LocalStorageCache: auth0SpaJs.LocalStorageCache,
  createAuthGuard: createAuthGuard,
  authGuard: authGuard
});

module.exports = Auth0Vue;
//# sourceMappingURL=auth0-vue.cjs.js.map
