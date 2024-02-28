import type { App, Ref } from 'vue';
import type { AppState, Auth0PluginOptions, Auth0VueClient, Auth0VueClientOptions, LogoutOptions, RedirectLoginOptions } from './interfaces';
import type { GetTokenSilentlyOptions, GetTokenSilentlyVerboseResponse, GetTokenWithPopupOptions, IdToken, PopupConfigOptions, PopupLoginOptions, RedirectLoginResult } from '@auth0/auth0-spa-js';
import { User } from '@auth0/auth0-spa-js';
/**
 * @ignore
 */
export declare const client: Ref<Auth0VueClient>;
/**
 * @ignore
 */
export declare class Auth0Plugin implements Auth0VueClient {
    private clientOptions;
    private pluginOptions?;
    private _client;
    isLoading: Ref<boolean>;
    isAuthenticated: Ref<boolean>;
    user: Ref<User | undefined>;
    idTokenClaims: Ref<IdToken | undefined>;
    error: Ref<{
        name: string;
        message: string;
        stack?: string | undefined;
    } | null>;
    constructor(clientOptions: Auth0VueClientOptions, pluginOptions?: Auth0PluginOptions | undefined);
    install(app: App): void;
    loginWithRedirect(options?: RedirectLoginOptions<AppState>): Promise<void>;
    loginWithPopup(options?: PopupLoginOptions, config?: PopupConfigOptions): Promise<void>;
    logout(options?: LogoutOptions): Promise<void>;
    getAccessTokenSilently(options: GetTokenSilentlyOptions & {
        detailedResponse: true;
    }): Promise<GetTokenSilentlyVerboseResponse>;
    getAccessTokenSilently(options?: GetTokenSilentlyOptions): Promise<string>;
    getAccessTokenWithPopup(options?: GetTokenWithPopupOptions, config?: PopupConfigOptions): Promise<string | undefined>;
    checkSession(options?: GetTokenSilentlyOptions): Promise<void>;
    handleRedirectCallback(url?: string): Promise<RedirectLoginResult<AppState>>;
    private __checkSession;
    private __refreshState;
    private __proxy;
}
