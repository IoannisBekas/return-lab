import { useMemo } from "react";
import katex from "katex";

type MathTextProps = {
  latex: string;
  display?: boolean;
  className?: string;
};

export function MathText({ latex, display = false, className = "" }: MathTextProps) {
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

  return (
    <Element
      className={`math-text${display ? " math-text--display" : ""}${className ? ` ${className}` : ""}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
