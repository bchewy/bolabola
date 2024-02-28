import type { RouteLocation } from 'vue-router';
import type { App } from 'vue';
import type { RedirectLoginOptions } from '@auth0/auth0-spa-js';
/**
 * The options used when creating an AuthGuard.
 */
export interface AuthGuardOptions {
    /**
     * The vue application
     */
    app?: App;
    /**
     * Route specific options to use when being redirected to Auth0
     */
    redirectLoginOptions?: RedirectLoginOptions;
}
/**
 *
 * @param [app] The vue application
 */
export declare function createAuthGuard(app?: App): (to: RouteLocation) => Promise<boolean>;
/**
 *
 * @param [options] The options used when creating an AuthGuard.
 */
export declare function createAuthGuard(options?: AuthGuardOptions): (to: RouteLocation) => Promise<boolean>;
export declare function authGuard(to: RouteLocation): Promise<boolean>;
