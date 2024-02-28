/**
 * @ignore
 * Run watchEffect untill the watcher returns true, then stop the watch.
 * Once it returns true, the promise will resolve.
 */
export declare function watchEffectOnceAsync<T>(watcher: () => T): Promise<void>;
/**
 * @ignore
 * Run watchEffect untill the watcher returns true, then stop the watch.
 * Once it returns true, it will call the provided function.
 */
export declare function watchEffectOnce<T>(watcher: () => T, fn: Function): void;
/**
 * @ignore
 * Helper function to bind methods to itself, useful when using Vue's `provide` / `inject` API's.
 */
export declare function bindPluginMethods(plugin: any, exclude: string[]): void;
/**
 * @ignore
 * Helper function to map the v1 `redirect_uri` option to the v2 `authorizationParams.redirect_uri`
 * and log a warning.
 */
export declare function deprecateRedirectUri(options?: any): void;
