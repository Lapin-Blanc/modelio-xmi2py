from __future__ import annotations

from dataclasses import dataclass, field

from modelio_xmi2py.ir.xmi import XmiDocument, XmiNode


@dataclass(slots=True)
class ResolveContext:
    doc: XmiDocument
    by_id: dict[str, XmiNode]
    unresolved: list[str] = field(default_factory=list)

    def resolve_id(self, xmi_id: str) -> XmiNode | None:
        return self.by_id.get(xmi_id)

    def split_href(self, href: str) -> tuple[str | None, str | None]:
        if "#" in href:
            path, fragment = href.rsplit("#", 1)
            return (path or None), (fragment or None)
        return href, None
    
    def resolve_href(self, href: str) -> tuple[str | None, str | None]:
        # Deprecated alias
        return self.split_href(href)

    def resolve_xmi_ref(self, value: str) -> XmiNode | None:
        if "#" in value:
            _, fragment = self.split_href(value)
            if fragment:
                resolved = self.by_id.get(fragment)
                if resolved is None:
                    self.unresolved.append(value)
                return resolved
            self.unresolved.append(value)
            return None
        resolved = self.by_id.get(value)
        if resolved is None:
            self.unresolved.append(value)
        return resolved
