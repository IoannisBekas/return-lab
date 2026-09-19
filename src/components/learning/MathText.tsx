import { useLayoutEffect, useMemo, useRef } from "react";
import katex from "katex";

type MathTextProps = {
  latex: string;
  display?: boolean;
  className?: string;
};

export function MathText({ latex, display = false, className = "" }: MathTextProps) {
  const elementRef = useRef<HTMLDivElement | HTMLSpanElement>(null);
  const html = useMemo(
    () =>
      katex.renderToString(latex, {
        displayMode: display,
        output: "htmlAndMathml",
        strict: "ignore",
        throwOnError: true,
      }),
    [display, latex],
  );

  const Element = display ? "div" : "span";

  useLayoutEffect(() => {
    if (!display || !elementRef.current) return;
    const container = elementRef.current;
    const equation = container.querySelector<HTMLElement>(".katex-display");
    if (!equation) return;
    const fit = () => {
      container.style.height = "auto";
      equation.style.removeProperty("transform");
      equation.style.removeProperty("transform-origin");
      equation.style.removeProperty("width");
      const available = container.clientWidth;
      const naturalWidth = equation.scrollWidth;
      if (!available || naturalWidth <= available) return;
      const scale = available / naturalWidth;
      const naturalHeight = equation.getBoundingClientRect().height;
      equation.style.transformOrigin = "top left";
      equation.style.transform = `scale(${scale})`;
      equation.style.width = `${100 / scale}%`;
      container.style.height = `${naturalHeight * scale}px`;
    };
    fit();
    const observer = new ResizeObserver(fit);
    observer.observe(container);
    return () => observer.disconnect();
  }, [display, html]);

  return (
    <Element
      ref={elementRef as never}
      className={`math-text${display ? " math-text--display" : ""}${className ? ` ${className}` : ""}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
