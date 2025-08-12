// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded "><a href="front-matter.html"><strong aria-hidden="true">1.</strong> Front Matter</a></li><li class="chapter-item expanded "><a href="chapters/chapter-01-the-perfect-lesson.html"><strong aria-hidden="true">2.</strong> Chapter 1 — The Perfect Lesson</a></li><li class="chapter-item expanded "><a href="chapters/chapter-02-system-flags.html"><strong aria-hidden="true">3.</strong> Chapter 2 — System Flags</a></li><li class="chapter-item expanded "><a href="chapters/chapter-03-home-compliance.html"><strong aria-hidden="true">4.</strong> Chapter 3 — Home Compliance</a></li><li class="chapter-item expanded "><a href="chapters/chapter-04-the-forgotten-library.html"><strong aria-hidden="true">5.</strong> Chapter 4 — The Forgotten Library</a></li><li class="chapter-item expanded "><a href="chapters/chapter-05-the-watchers.html"><strong aria-hidden="true">6.</strong> Chapter 5 — The Watchers</a></li><li class="chapter-item expanded "><a href="chapters/chapter-06-the-first-broadcast.html"><strong aria-hidden="true">7.</strong> Chapter 6 — The First Broadcast</a></li><li class="chapter-item expanded "><a href="chapters/chapter-07-the-ministry-responds.html"><strong aria-hidden="true">8.</strong> Chapter 7 — The Ministry Responds</a></li><li class="chapter-item expanded "><a href="chapters/chapter-08-code-in-the-cracks.html"><strong aria-hidden="true">9.</strong> Chapter 8 — Code in the Cracks</a></li><li class="chapter-item expanded "><a href="chapters/chapter-09-operation-contradiction.html"><strong aria-hidden="true">10.</strong> Chapter 9 — Operation Contradiction</a></li><li class="chapter-item expanded "><a href="chapters/chapter-10-capture.html"><strong aria-hidden="true">11.</strong> Chapter 10 — Capture</a></li><li class="chapter-item expanded "><a href="chapters/chapter-11-the-core.html"><strong aria-hidden="true">12.</strong> Chapter 11 — The Core</a></li><li class="chapter-item expanded "><a href="chapters/chapter-12-the-wrong-answer-that-saved-the-world.html"><strong aria-hidden="true">13.</strong> Chapter 12 — The Wrong Answer That Saved the World</a></li><li class="chapter-item expanded "><a href="book_outline.html"><strong aria-hidden="true">14.</strong> Appendix — Outline</a></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
