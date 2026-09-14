/**
 * Antigravity IDE - Cross-Platform Path & String Utilities (Zero Dependency)
 */

export class PathUtils {
  public static normalize(p: string): string {
    return p.replace(/\\/g, '/').replace(/\/+/g, '/');
  }

  public static basename(p: string): string {
    const normalized = PathUtils.normalize(p).replace(/\/$/, '');
    const idx = normalized.lastIndexOf('/');
    return idx === -1 ? normalized : normalized.substring(idx + 1);
  }

  public static isSubdirectory(parent: string, child: string): boolean {
    const normParent = PathUtils.normalize(parent).replace(/\/$/, '') + '/';
    const normChild = PathUtils.normalize(child);
    return normChild.startsWith(normParent);
  }
}
