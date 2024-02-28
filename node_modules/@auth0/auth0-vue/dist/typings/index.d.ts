import './global';
import { Auth0Plugin } from './global';
import type { Auth0VueClient, Auth0PluginOptions, Auth0VueClientOptions } from './global';
import { AUTH0_TOKEN } from './token';
export * from './global';
export { AUTH0_INJECTION_KEY } from './token';
declare module '@vue/runtime-core' {
    interface ComponentCustomProperties {
        [AUTH0_TOKEN]: Auth0VueClient;
    }
}
/**
 * Creates the Auth0 plugin.
 *
 * @param clientOptions The Auth Vue Client Options
 * @param pluginOptions Additional Plugin Configuration Options
 * @returns An instance of Auth0Plugin
 */
export declare function createAuth0(clientOptions: Auth0VueClientOptions, pluginOptions?: Auth0PluginOptions): Auth0Plugin;
/**
 * Returns the registered Auth0 instance using Vue's `inject`.
 * @returns An instance of Auth0VueClient
 */
export declare function useAuth0(): Auth0VueClient;
