type BrandMarkProps = {
  className?: string;
  compact?: boolean;
};

export default function BrandMark({ className = "", compact = false }: BrandMarkProps) {
  return (
    <svg
      viewBox="0 0 360 360"
      className={className}
      role="img"
      aria-label="ProspectAI logo"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M104 46h52v268h-52V46Zm52 0h88c73 0 128 44 128 108 0 65-55 108-128 108h-88V46Zm45 55h38c31 0 48 15 48 40 0 24-17 40-48 40h-38V101Zm-44 62v104h25c50 0 83-22 83-61 0-41-33-63-83-63h-25Z"
        fill="currentColor"
        transform={compact ? "translate(0 4) scale(0.9)" : "translate(0 0)"}
      />
      <circle cx="242" cy="220" r="22" fill="currentColor" />
    </svg>
  );
}
