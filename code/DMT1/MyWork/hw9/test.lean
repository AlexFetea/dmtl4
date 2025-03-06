universe u
variable (A : Type u)

inductive P_pred (a : A) : Prop where
| mk : P_pred a

inductive Q_pred (a : A) : Prop where
| mk : Q_pred a

inductive R_pred (a : A) : Prop where
| mk : R_pred a

inductive N_pred (a : A) : Prop  -- No constructors, so always false.

example : ∀ x : A, (P_pred x ∧ (Q_pred x ∧ R_pred x)) → (P_pred x ∧ Q_pred x) ∧ R_pred x :=
  fun x h =>
    -- Explicitly reference x so the editor knows it's used:
    let _ : A := x
    let p := h.left
    let qr := h.right
    let q := qr.left
    let r := qr.right
    ⟨⟨p, q⟩, r⟩
