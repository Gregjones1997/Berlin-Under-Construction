export function requireLegalAddress(value: string | undefined): string {
  if (!value?.trim() || /\[\[|\]\]/.test(value)) {
    throw new Error(
      "LEGAL_ADDRESS must contain the owner's complete serviceable postal address",
    );
  }
  return value.trim();
}
